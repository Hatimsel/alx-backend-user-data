#!/usr/bin/env python3
"""Logging in Python"""
import logging
import re
from typing import List


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
        logging.basicConfig(format=self.FORMAT)

        new_record = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        
        logging.info(new_record)
        # org_msg = super().format(record)

        # return filter_datum(self.fields, self.REDACTION,
        #                     org_msg, self.SEPARATOR)
