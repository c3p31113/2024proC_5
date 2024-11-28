from typing import Any
from json import dumps, loads

from logging import getLogger
from uvicorn import run as uvicornrun
from pydantic import BaseModel, ValidationError
from pydantic.json import pydantic_encoder

from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from databases import literals as databaseliterals
from databases.accessor import connect, selectFrom, insertInto
import security.authenticate as auth


PORT = 3000
RELOAD = True  # 編集しファイルを保存するたびにサーバーを自動再起動するか

logger = getLogger("uvicorn.app")
app = FastAPI()
print = logger.info  # ポインタって素晴らしい

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    uvicornrun(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=RELOAD,
        log_config="config/log_config.yaml",
    )


class APIResponse(BaseModel):
    message: str
    body: Any = None


class Product(BaseModel):
    ID: int
    name: str
    summary: str | None
    desc: str | None
    product_categories_ID: int
    yen_per_kg: int
    yen_per_1a: int

    @staticmethod
    def all_from_DB() -> "list[Product]":
        connection = connect()
        products = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_PRODUCTS,
            "*",
        )
        connection.close()
        if products is None:
            raise EXCEPTION_FAILED_TO_CONNECT_DB
        result: list[Product] = []
        for product in products:
            result.append(Product(**product))
        return result

    @staticmethod
    def one_from_DB(id: int) -> "Product | None":
        if id is None:
            raise EXCEPTION_BLANK_QUERY
        connection = connect()
        product = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_PRODUCTS,
            "*",
            f"ID = {id}",
            True,
        )
        connection.close()
        return Product(**product)


class Contact(BaseModel):
    ID: int
    email_address: str
    form_id: int | None = None
    title: str
    content: str

    @staticmethod
    def all_from_DB() -> "list[Contact]":
        connection = connect()
        contacts = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_CONTACTS,
            "*",
        )
        connection.close()
        if contacts is None:
            raise EXCEPTION_FAILED_TO_CONNECT_DB

        result: list[Contact] = []
        for contact in contacts:
            instance = Contact(**contact)
            result.append(instance)
        return result

    @staticmethod
    def one_from_DB(id: int) -> "Contact | None":
        connection = connect()
        contact = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_CONTACTS,
            "*",
            f"ID = {id}",
            True,
        )
        if contact is None:
            return None
        connection.close()
        return Contact(**contact)


class Form(BaseModel):
    class ProductInForm(BaseModel):
        id: int
        amount: float

        def get_product(self) -> Product | None:
            return Product.one_from_DB(self.id)

    id: int
    product_array: list[ProductInForm]
    manpower: int

    def get_Products(self) -> list[Product | None]:
        result = []
        for product in self.product_array:
            result.append(product.get_product())
        return result

    @staticmethod
    def all_from_DB() -> "list[Form]":
        connection = connect()
        forms = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_FORM,
            "*",
        )
        connection.close()
        if forms is None:
            raise EXCEPTION_FAILED_TO_CONNECT_DB

        result: list[Form] = []
        for contact in forms:
            instance = Form(**contact)
            result.append(instance)
        return result

    @staticmethod
    def one_from_DB(id: int) -> "Form | None":
        connection = connect()
        form = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_FORM,
            "*",
            f"ID = {id}",
            True,
        )
        if form is None:
            return None
        connection.close()
        product_array: list[Form.ProductInForm] = []
        try:
            for product in loads(form["product_array"]):
                result = Form.ProductInForm(**product)
                product_array.append(result)
        except ValidationError:
            return None
        return Form(
            id=form["ID"], product_array=product_array, manpower=form["manpower"]
        )


EXCEPTION_FAILED_TO_CONNECT_DB = HTTPException(
    detail="couldn't connect to database",
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
)
EXCEPTION_BLANK_CLIENT_IP = HTTPException(
    detail="somehow you are non-existance client. couldn't get your IP",
    status_code=status.HTTP_400_BAD_REQUEST,
)
EXCEPTION_BLANK_QUERY = HTTPException(
    detail="query was blank",
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
)
EXCEPTION_REQUEST_INVALID = HTTPException(
    detail="request form was invalid to read. check data structure",
    status_code=status.HTTP_400_BAD_REQUEST,
)
EXCEPTION_REQUEST_FAILED_TO_PROCESS = HTTPException(
    detail="request was failed to process.",
    status_code=status.HTTP_400_BAD_REQUEST,
)

RESPONSE_REQUEST_PROCESSED = APIResponse(
    message="request was processed successfully.", body=True
)
RESPONSE_NO_MATCH_IN_DB = APIResponse(
    message="specified id wasn't found in the table", body=False
)


def log_accessor(request: Request) -> None:
    request_path = request.scope["path"]
    if request.client is None:
        raise EXCEPTION_BLANK_CLIENT_IP
    logger.debug(f"{request.client.host} has accessed to {request_path}")
    request_params = request.scope["query_string"]
    if request_params:
        logger.debug(f"params were {request_params}")


@app.get("/")
def root(_request: None = Depends(log_accessor)) -> APIResponse:
    test = {
        "message": "this is 2024proc sd5 API powered by fastAPI. check /docs page for documents",
        "body": True,
    }
    return APIResponse(**test)


@app.get("/v1/")
def v1_root() -> APIResponse:
    return APIResponse(message="this is 2024proc sd5 API, version 1")


@app.get("/v1/products")
def get_products(
    _request: None = Depends(log_accessor),
    products: list[Product] = Depends(Product.all_from_DB),
) -> APIResponse:
    return APIResponse(message="ok", body=products)


@app.get("/v1/products/{id}")
def get_product(
    _request: None = Depends(log_accessor),
    product: Product = Depends(Product.one_from_DB),
) -> APIResponse:
    logger.debug(product)
    if product is None:
        return RESPONSE_NO_MATCH_IN_DB
    return APIResponse(message="ok", body=product)


@app.get("/v1/productCategories")
def get_product_categories(_request: None = Depends(log_accessor)) -> APIResponse:
    connection = connect()
    productCategories = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        "*",
    )
    connection.close()
    if productCategories is None:
        raise EXCEPTION_FAILED_TO_CONNECT_DB
    return APIResponse(message="ok", body=productCategories)


@app.get("/v1/productCategories/{id}")
def get_product_category(
    _request: None = Depends(log_accessor),
    id: int | None = None,
) -> APIResponse:
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    connection = connect()
    productCategory = selectFrom(
        connection,
        databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
        "*",
        f"ID = {id}",
        True,
    )
    if productCategory is None:
        return RESPONSE_NO_MATCH_IN_DB
    connection.close()
    logger.info(productCategory)
    if productCategory["ID"] == id:
        return APIResponse(message="ok", body=productCategory)
    return RESPONSE_NO_MATCH_IN_DB


@app.get("/v1/forms/{id}")
def get_form(
    id: int | None = None,
    form: Form = Depends(Form.one_from_DB),
    detailedmode: bool = False,
    _request: None = Depends(log_accessor),
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
) -> APIResponse:
    logger.info(f"{current_admin.username} has accessed to form specifying {id}")
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    if form is None:
        return RESPONSE_NO_MATCH_IN_DB
    if detailedmode:
        return APIResponse(
            message="ok",
            body={
                "id": form.id,
                "product_array_detailed": form.get_Products(),
                "manpower": form.manpower,
            },
        )
    else:
        return APIResponse(message="ok", body=form)


@app.post("/v1/forms", status_code=status.HTTP_201_CREATED)
def post_form(
    form: Form,
    _request: None = Depends(log_accessor),
) -> APIResponse:
    if not type(form.product_array) is list or not type(form.manpower) is int:
        raise EXCEPTION_REQUEST_INVALID
    connection = connect()
    logger.debug(form)
    result = insertInto(
        connection,
        "form",
        ["product_array", "manpower"],
        [
            f"{dumps(form.product_array, default=pydantic_encoder).replace('"', "\\\"")}",
            form.manpower,
        ],
    )
    connection.close()
    if result:
        return RESPONSE_REQUEST_PROCESSED
    else:
        raise EXCEPTION_REQUEST_FAILED_TO_PROCESS


@app.post("/v1/contacts", status_code=status.HTTP_201_CREATED)
def post_contact(
    contact: Contact,
    _request: None = Depends(log_accessor),
) -> APIResponse:
    connection = connect()
    result = insertInto(
        connection,
        "contacts",
        [
            "email_address",
            "form_id",
            "title",
            "content",
        ],
        [
            contact.email_address,
            contact.form_id,
            contact.title,
            contact.content,
        ],
    )
    connection.close()
    logger.debug(contact)
    if result:
        return RESPONSE_REQUEST_PROCESSED
    else:
        raise EXCEPTION_REQUEST_FAILED_TO_PROCESS


@app.get("/v1/contacts")
def get_contacts(
    contacts: list[Contact] = Depends(Contact.all_from_DB),
    _request: None = Depends(log_accessor),
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
) -> APIResponse:
    return APIResponse(message="ok", body=contacts)


@app.get("/v1/contacts/{id}")
def get_contact(
    contact: Contact | None = Depends(Contact.one_from_DB),
    _request: None = Depends(log_accessor),
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
) -> APIResponse:
    if contact is None:
        return RESPONSE_NO_MATCH_IN_DB
    return APIResponse(message="ok", body=contact)


@app.post("/v1/token")
async def login_for_access_token(
    _request: None = Depends(log_accessor),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> auth.Token:
    admin = auth.authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise auth.EXCEPTION_INCORRECT_USER_OR_PASS
    access_token = auth.create_access_token(data={"sub": admin.username})
    return auth.Token(access_token=access_token, token_type="bearer")


@app.get("/v1/admin/me", response_model=auth.Admin)
async def read_admin_me(
    current_admin: auth.Admin = Depends(auth.get_current_active_user),
):
    return current_admin


if __name__ == "__main__":
    main()
