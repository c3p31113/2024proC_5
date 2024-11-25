from typing import Any
from json import load
from logging import getLogger
from mysql.connector import MySQLConnection, errors as MYSQLerrors

logger = getLogger("uvicorn.app")


def jsonload(filepath: str):
    with open(filepath, mode="r") as file:
        result = load(file)
    return result


def connect(configpath="./config/dbconfig.json"):
    config = jsonload(configpath)
    return MySQLConnection(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        collation="utf8mb4_general_ci",
    )


def selectFrom(
    connection: MySQLConnection,
    table: str,
    columns: str | list[str],
    where: str = "",
    oneOnly: bool = False,
) -> Any:
    cursor = connection.cursor(dictionary=True)
    if type(columns) is list:
        columns = ", ".join(columns)
    query = f"SELECT {columns} FROM {table}"
    if where != "":
        query = f"{query} WHERE {where}"
    try:
        cursor.execute(query)
    except MYSQLerrors.ProgrammingError:
        logger.error(f"query failed to run: {query}")
        return None
    if oneOnly:
        result = cursor.fetchall()[0]
    else:
        result = cursor.fetchall()
    cursor.close()
    return result


def insertInto(
    connection: MySQLConnection,
    table: str,
    columns: list[str],
    values: list[str | int | None],
) -> bool:
    if len(columns) != len(values):
        logger.info("different len between columns and values")
        return False
    cursor = connection.cursor(dictionary=True)
    value_result = []
    columns_result = []
    for i, value in enumerate(values):
        if value is None:
            continue
        if type(value) is int or (type(value) is str and value.isdecimal()):
            value_result.append(str(value))
        elif type(value) is str and (
            not value.startswith('"') and not value.endswith('"')
        ):
            value_result.append(f'"{value}"')
        columns_result.append(columns[i])
        continue
    query = f"INSERT INTO {table} ({", ".join(columns_result)}) VALUES ({", ".join(value_result)})"
    logger.debug(query)
    try:
        cursor.execute(query)
    except MYSQLerrors.ProgrammingError:
        logger.error(f"query failed to run: {query}")
        return False
    connection.commit()
    cursor.close()
    return True


def update(
    connection: MySQLConnection,
    table: str,
    column: str,
    value: str,
    where: str = "",
) -> bool:
    cursor = connection.cursor(dictionary=True)
    query = f"UPDATE {table} SET {column} = {value}"
    if where != "":
        query = f"{query} WHERE {where}"
    try:
        cursor.execute(query)
    except MYSQLerrors.ProgrammingError:
        logger.error(f"query failed to run: {query}")
        return False
    cursor.close()
    return True
