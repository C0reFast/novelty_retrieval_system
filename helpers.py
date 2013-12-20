#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Project helpers"""

from config import OPTIONS
import _mssql
import pymssql


def mssqlconn():
    """Get _mssql connection object"""
    return _mssql.connect(
        server=OPTIONS.get('db', 'server'),
        user=OPTIONS.get('db', 'user'),
        password=OPTIONS.get('db', 'password'),
        database=OPTIONS.get('db', 'database'),
        port=OPTIONS.getint('db', 'port'),
        )


def pymssqlconn():
    """Get pymssql connection object"""
    return pymssql.connect(
        server=OPTIONS.get('db', 'server'),
        user=OPTIONS.get('db', 'user'),
        password=OPTIONS.get('db', 'password'),
        database=OPTIONS.get('db', 'database'),
        port=OPTIONS.getint('db', 'port'),
        )
