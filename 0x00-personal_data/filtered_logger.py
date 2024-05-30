#!/usr/bin/env python3
"""Logging in Python"""
import logging
from mysql.connector import MySQLConnection, Error
import os
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates the log message passed
    and returns the result
    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]+)"

    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records"""
        org_msg = super().format(record)

        return filter_datum(self.fields, self.REDACTION,
                            org_msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creating a logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database"""
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pass = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')

    try:
        connection = MySQLConnection(user=db_user, password=db_pass,
                                     host=db_host, database=db_name)
        return connection

    except Error as e:
        print(f'Error: {e}')
        return None


def main() -> None:
    """
    Gets the db connection and retrives all
    rows in the user table
    """
    db = get_db()
    cursor = db.cursor()
    query = 'SELECT name, email, phone, ssn, password FROM users'
    cursor.execute(query)

    result = cursor.fetchall()

    instance = RedactingFormatter(list(PII_FIELDS))
    for row in result:
        row = instance.format(row)
        print(row)


if __name__ == '__main__':
    main()
