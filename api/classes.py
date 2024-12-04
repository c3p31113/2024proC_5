from json import loads
from exceptions import EXCEPTION_FAILED_TO_CONNECT_DB
from databases import literals as databaseliterals
from databases.accessor import connect, selectFrom
from exceptions import EXCEPTION_BLANK_QUERY


from pydantic import BaseModel, ValidationError


class Product(BaseModel):
    ID: int
    name: str
    summary: str | None
    desc: str | None
    product_categories_ID: int
    yen_per_kg: int
    kg_per_1a: int

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


class ProductCategory(BaseModel):
    ID: int
    name: str
    summary: str | None

    @staticmethod
    def all_from_DB() -> "list[ProductCategory]":
        connection = connect()
        product_categories = selectFrom(
            connection,
            databaseliterals.DATABASE_TABLE_PRODUCTCATEGORIES,
            "*",
        )
        connection.close()
        if product_categories is None:
            raise EXCEPTION_FAILED_TO_CONNECT_DB
        result: list[ProductCategory] = []
        for product_category in product_categories:
            result.append(ProductCategory(**product_category))
        return result

    @staticmethod
    def one_from_DB(id: int) -> "ProductCategory | None":
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
        connection.close()
        return ProductCategory(**productCategory)


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

    def get_Products(self) -> list[Product]:
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
