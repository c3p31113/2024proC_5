from typing import Any
from json import load
from logging import getLogger
from mysql.connector import MySQLConnection, errors as MYSQLerrors
from mysql.connector.cursor import MySQLCursor

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


def selectCursor(
    connection: MySQLConnection, table: str, columns: str | list[str], where: str = ""
) -> MySQLCursor:
    cursor = connection.cursor(dictionary=True)
    if columns is str:
        query_columns = columns
    else:
        query_columns = " ".join(columns)
    if where != "":
        query = f"SELECT {query_columns} FROM {table} WHERE {where}"
    else:
        query = f"SELECT {query_columns} FROM {table}"
    try:
        cursor.execute(query)
    except MYSQLerrors.ProgrammingError:
        logger.error(f"query failed to run: {query}")
    return cursor


def selectAllFrom(
    connection: MySQLConnection,
    table: str,
    columns: str | list[str],
    where: str = "",
) -> list[dict[str, Any] | Any] | None:
    cursor = selectCursor(connection, table, columns, where)
    result = cursor.fetchall()
    cursor.close()
    return result


def selectOneFrom(
    connection: MySQLConnection,
    table: str,
    columns: str | list[str],
    where: str = "",
) -> dict[str, Any] | Any | None:
    cursor = selectCursor(connection, table, columns, where)
    result = cursor.fetchone()
    cursor.close()
    return result


def insertInto(
    connection: MySQLConnection,
    table: str,
    columns: list[str],
    values: list[str],
) -> None:  # TODO 未動作検証
    cursor = connection.cursor(dictionary=True)
    query = f"INSERT INTO {table} ({" ".join(columns)}) VALUES ({" ".join(values)})"
    cursor.execute(query)
    connection.commit()
    cursor.close()
