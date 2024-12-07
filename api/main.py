from typing import Any
from json import dumps, load
from os import system as shell

from logging import getLogger
from uvicorn import run as uvicornrun
from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from fastapi import FastAPI, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from exceptions import (
    EXCEPTION_BLANK_CLIENT_IP,
    EXCEPTION_BLANK_QUERY,
    EXCEPTION_REQUEST_FAILED_TO_PROCESS,
    EXCEPTION_REQUEST_INVALID,
)
from classes import Contact, Form, Product, ProductCategory
from databases import literals as databaseliterals
from databases.accessor import connect, insertInto, update
import security.authenticate as auth
from make_doc import main as make_docer


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
def get_product_categories(
    _request: None = Depends(log_accessor),
    productCategories: list[ProductCategory] = Depends(ProductCategory.all_from_DB),
) -> APIResponse:
    if productCategories is None:
        return RESPONSE_NO_MATCH_IN_DB
    return APIResponse(message="ok", body=productCategories)


@app.get("/v1/productCategories/{id}")
def get_product_category(
    id: int | None = None,
    _request: None = Depends(log_accessor),
    productCategory: ProductCategory = Depends(ProductCategory.one_from_DB),
) -> APIResponse:
    logger.debug(productCategory)
    if id is None:
        raise EXCEPTION_BLANK_QUERY
    if productCategory is None:
        return RESPONSE_NO_MATCH_IN_DB
    return APIResponse(message="ok", body=productCategory)


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
    make_docer(form)
    if result is not None:
        return APIResponse(
            message="request was processed successfully.", body={"lastrowid": result}
        )
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


@app.get("/v1/scrape")
async def get_scrape(
    # current_admin: auth.Admin = Depends(auth.get_current_active_user),
):
    FILENAME = "./tmp/output.json"
    shell(f"python api/scraper/agriculture_scraper.py => {FILENAME}")
    logger.info("scraped.")
    with open(FILENAME, mode="r") as file:
        scraped_data: list[dict] = load(file)
    for product in scraped_data:
        update(
            connection=connect(),
            table=databaseliterals.DATABASE_TABLE_PRODUCTS,
            column="yen_per_kg",
            value=product["price"],
            where=f"id={product["id"]}",
        )
    return APIResponse(message="ok", body=scraped_data)


@app.get("/v1/get_file")
async def get_result_file(_request: None = Depends(log_accessor)) -> FileResponse:
    return FileResponse(
        headers={"Content-Disposition": "attachment;"},
        path="./tmp/Result.docx",
        filename="result.docx",
    )


if __name__ == "__main__":
    main()
