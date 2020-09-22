# -*- coding: utf-8 -*-

import datetime
from mehdi_lib.basics import basic_types

import dateutil.parser
from PyQt5 import QtSql

from mehdi_lib.tools import tools


# ===========================================================================
class Database:
    # noinspection PyCallByClass,PyTypeChecker,SpellCheckingInspection
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('./db.sqlite')
    reserved_words = [
        "ABORT",
        "ACTION",
        "ADD",
        "AFTER",
        "ALL",
        "ALTER",
        "ANALYZE",
        "AND",
        "AS",
        "ASC",
        "ATTACH",
        "AUTOINCREMENT",
        "BEFORE",
        "BEGIN",
        "BETWEEN",
        "BY",
        "CASCADE",
        "CASE",
        "CAST",
        "CHECK",
        "COLLATE",
        "COLUMN",
        "COMMIT",
        "CONFLICT",
        "CONSTRAINT",
        "CREATE",
        "CROSS",
        "CURRENT_DATE",
        "CURRENT_TIME",
        "CURRENT_TIMESTAMP",
        "DATABASE",
        "DEFAULT",
        "DEFERRABLE",
        "DEFERRED",
        "DELETE",
        "DESC",
        "DETACH",
        "DISTINCT",
        "DROP",
        "EACH",
        "ELSE",
        "END",
        "ESCAPE",
        "EXCEPT",
        "EXCLUSIVE",
        "EXISTS",
        "EXPLAIN",
        "FAIL",
        "FOR",
        "FOREIGN",
        "FROM",
        "FULL",
        "GLOB",
        "GROUP",
        "HAVING",
        "IF",
        "IGNORE",
        "IMMEDIATE",
        "IN",
        "INDEX",
        "INDEXED",
        "INITIALLY",
        "INNER",
        "INSERT",
        "INSTEAD",
        "INTERSECT",
        "INTO",
        "IS",
        "ISNULL",
        "JOIN",
        "KEY",
        "LEFT",
        "LIKE",
        "LIMIT",
        "MATCH",
        "NATURAL",
        "NO",
        "NOT",
        "NOTNULL",
        "NULL",
        "OF",
        "OFFSET",
        "ON",
        "OR",
        "ORDER",
        "OUTER",
        "PLAN",
        "PRAGMA",
        "PRIMARY",
        "QUERY",
        "RAISE",
        "RECURSIVE",
        "REFERENCES",
        "REGEXP",
        "REINDEX",
        "RELEASE",
        "RENAME",
        "REPLACE",
        "RESTRICT",
        "RIGHT",
        "ROLLBACK",
        "ROW",
        "SAVEPOINT",
        "SELECT",
        "SET",
        "TABLE",
        "TEMP",
        "TEMPORARY",
        "THEN",
        "TO",
        "TRANSACTION",
        "TRIGGER",
        "UNION",
        "UNIQUE",
        "UPDATE",
        "USING",
        "VACUUM",
        "VALUES",
        "VIEW",
        "VIRTUAL",
        "WHEN",
        "WHERE",
        "WITH",
        "WITHOUT",
    ]
    types = {
        str: "VARCHAR",
        int: "INTEGER",
        float: "REAL",
        datetime.date: "DATETIME",
        datetime.datetime: "DATETIME",
        datetime.timedelta: "DATETIME",
        bool: "INTEGER",
        basic_types.UiTitleEnabledEnum: "INTEGER"
    }


# ===========================================================================
class Types:

    enum_None_in_database = -1

    # ===========================================================================
    @staticmethod
    def format_for_database(value, type_in_class):
        if type_in_class == bool:
            if value:
                return 1
            else:
                return 0
        if type_in_class in [str, datetime.datetime, datetime.date]:
            return '"{}"'.format(value)
        if issubclass(type_in_class, basic_types.UiTitleEnabledEnum):
            if value is None:
                return Types.enum_None_in_database
            return value.value
        if type_in_class == datetime.timedelta:
            hours = value.seconds // 3600 + value.days * 24
            minutes = (value.seconds // 60) % 60
            seconds = value.seconds % 60
            return '"{}:{}:{}"'.format(hours, minutes, seconds)

        return value

    # ===========================================================================
    @staticmethod
    def format_for_class(value, type_in_class):
        new_value = value

        if type_in_class is bool:
            if value:
                new_value = True
            else:
                new_value = False

        if issubclass(type_in_class, basic_types.UiTitleEnabledEnum):
            if value == Types.enum_None_in_database:
                new_value = None
            else:
                new_value = type_in_class(value)
        if type_in_class is datetime.datetime:
            new_value = dateutil.parser.parse(value)
        if type_in_class is datetime.date:
            new_value = dateutil.parser.parse(value).date()

        if type_in_class is datetime.timedelta:
            try:
                hours, minutes, seconds, *extra = value.split(':')
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                # noinspection PyCallingNonCallable
                new_value = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except ValueError:
                raise ValueError('problem converting "{}" to timedelta'.format(value))

        return new_value


# ===========================================================================
class Conditions:
    not_null = "NOT NULL"
    unique = "UNIQUE"
    unique_not_null = "UNIQUE NOT NULL"
    primary_key = "PRIMARY KEY UNIQUE NOT NULL"
    primary_key_auto = "PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL"
    no_condition = ""


# ===========================================================================
class Commands:
    # ===========================================================================
    @staticmethod
    def exec_query(command: str) -> QtSql.QSqlQuery:
        if not Database.db:
            tools.Tools.warning('no database is specified')
            # noinspection PyTypeChecker
            return None
        if not Database.db.isOpen():
            if not Database.db.open():
                tools.Tools.warning('cannot open the database')
                # noinspection PyTypeChecker
                return None

        query = QtSql.QSqlQuery()
        if not query.exec(command):
            tools.Tools.warning('database query error:', query.lastError().text(), '\n', command)
            # noinspection PyTypeChecker
            return None

        return query

