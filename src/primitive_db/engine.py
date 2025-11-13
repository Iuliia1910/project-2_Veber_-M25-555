#!/usr/bin/env python3
import shlex
from src.primitive_db.core import (
    create_table, drop_table, list_tables,
    insert, select, update, delete, info
)
from src.primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from prettytable import PrettyTable


def print_help():
    """Выводит справку по всем командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("create_table <table_name> <col:type> ... - создать таблицу")
    print("list_tables - показать список всех таблиц")
    print("drop_table <table_name> - удалить таблицу")
    print("insert into <table_name> values (<v1>, <v2>, ...) - добавить запись")
    print("select from <table_name> [where <col>=<value>] - получить записи")
    print("update <table_name> set <col>=<val> where <col>=<val> - обновить запись")
    print("delete from <table_name> where <col>=<val> - удалить запись")
    print("info <table_name> - информация о таблице")
    print("\nОбщие команды:")
    print("exit - выход из программы")
    print("help - справочная информация\n")


def parse_where(args):
    """Парсинг where <col>=<value>"""
    if "where" in args:
        idx = args.index("where")
        clause = args[idx + 1]
        if "=" in clause:
            col, val = clause.split("=", 1)
            val = val.strip('"').strip("'")
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            return {col: val}
    return None


def parse_set(args):
    """Парсинг set <col>=<value>"""
    if "set" in args:
        idx = args.index("set")
        clause = args[idx + 1]
        if "=" in clause:
            col, val = clause.split("=", 1)
            val = val.strip('"').strip("'")
            if val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            return {col: val}
    return None


def run():
    print("***База данных***")
    while True:
        user_input = input(">>> Введите команду: ")
        args = shlex.split(user_input)
        if not args:
            continue

        command = args[0]

        metadata = load_metadata("db_meta.json")

        try:
            if command == "create_table":
                table_name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, table_name, columns)
                save_metadata("db_meta.json", metadata)

            elif command == "list_tables":
                list_tables(metadata)

            elif command == "drop_table":
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata("db_meta.json", metadata)

            elif command == "insert":
                if args[1] != "into":
                    print("Некорректная команда. Используйте: insert into <table> values (...)")
                    continue
                table_name = args[2]
                if args[3] != "values":
                    print("Некорректная команда. Используйте: insert into <table> values (...)")
                    continue
                values_str = user_input.split("values", 1)[1].strip().lstrip("(").rstrip(")")
                values = [v.strip().strip('"').strip("'") for v in values_str.split(",")]
                table_data = load_table_data(table_name)
                table_data = insert(metadata, table_name, values, table_data)
                save_table_data(table_name, table_data)

            elif command == "select":
                table_name = args[2]
                where_clause = parse_where(args)
                table_data = load_table_data(table_name)
                rows = select(table_data, where_clause)
                if rows:
                    cols = metadata[table_name]
                    table = PrettyTable()
                    table.field_names = cols.keys()
                    for r in rows:
                        table.add_row([r[c] for c in cols.keys()])
                    print(table)
                else:
                    print("Записей не найдено.")

            elif command == "update":
                table_name = args[1]
                set_clause = parse_set(args)
                where_clause = parse_where(args)
                table_data = load_table_data(table_name)
                table_data = update(table_data, set_clause, where_clause)
                save_table_data(table_name, table_data)

            elif command == "delete":
                table_name = args[2]
                where_clause = parse_where(args)
                table_data = load_table_data(table_name)
                table_data = delete(table_data, where_clause)
                save_table_data(table_name, table_data)

            elif command == "info":
                table_name = args[1]
                table_data = load_table_data(table_name)
                info(metadata, table_name, table_data)

            elif command == "help":
                print_help()

            elif command == "exit":
                break

            else:
                print(f"Функции {command} нет. Попробуйте снова.")

        except Exception as e:
            print("Ошибка:", e)

