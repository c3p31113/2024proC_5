from mysql.connector import MySQLConnection, errors as MYSQLerrors
from json import load


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


def selectfrom(conn: MySQLConnection, target: str):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {target}")
    except MYSQLerrors.ProgrammingError:
        print("the table doesn't exist!")
        return
    result = cursor.fetchall()
    cursor.close()
    return result


def main():
    connection = connect()
    print(selectfrom(connection, "admins"))
    connection.close()


main()
