#!/usr/bin/env python3
"""Logging in Python"""
import re


def filter_datum(fields: [str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates the log message passed
    and returns the result
    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]+)"

    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
