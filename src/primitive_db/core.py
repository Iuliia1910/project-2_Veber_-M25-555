# src/primitive_db/core.py
from prettytable import PrettyTable
from .utils import load_table_data, save_table_data

VALID_TYPES = {"int": int, "str": str, "bool": bool}

# ------------------------------
# Таблицы
# ------------------------------

def create_table(metadata, table_name, columns):
    """Создает таблицу с указанными столбцами и добавляет ID:int."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    # Проверка типов
    parsed_columns = []
    for col in columns:
        if ':' not in col:
            print(f'Некорректное значение: {col}. Попробуйте снова.')
            return metadata
        name, dtype = col.split(':', 1)
        if dtype not in VALID_TYPES:
            print(f'Некорректное значение: {dtype}. Попробуйте снова.')
            return metadata
        parsed_columns.append((name, dtype))

    # Добавляем ID:int в начало
    parsed_columns.insert(0, ("ID", "int"))

    metadata[table_name] = parsed_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join([f"{n}:{t}" for n, t in parsed_columns])}')
    return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    metadata.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """Выводит список таблиц."""
    if not metadata:
        print("Таблиц нет.")
        return
    for table in metadata:
        print(f"- {table}")

def info(metadata, table_name):
    """Вывод информации о таблице."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    columns = metadata[table_name]
    print(f"Таблица: {table_name}")
    print("Столбцы: " + ", ".join([f"{name}:{dtype}" for name, dtype in columns]))
    data = load_table_data(table_name)
    print(f"Количество записей: {len(data)}")

# ------------------------------
# CRUD
# ------------------------------

def insert(metadata, table_name, values):
    """Добавляет запись в таблицу."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    if len(values) != len(columns) - 1:  # минус ID
        print(f'Некорректное количество значений. Ожидается {len(columns)-1}, получено {len(values)}.')
        return

    # Валидация типов
    record = {"ID": 1}
    for (col_name, col_type), val in zip(columns[1:], values):
        py_type = VALID_TYPES[col_type]
        try:
            # конвертируем значение
            if col_type == "bool":
                if isinstance(val, str):
                    val = val.lower() in ["true", "1"]
            else:
                val = py_type(val)
        except Exception:
            print(f'Некорректное значение: {val}. Попробуйте снова.')
            return
        record[col_name] = val

    # Генерация ID
    data = load_table_data(table_name)
    if data:
        record["ID"] = max(d["ID"] for d in data) + 1
    data.append(record)
    save_table_data(table_name, data)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')

def select(table_data, where_clause=None):
    """Выбирает записи из таблицы."""
    if where_clause:
        result = [row for row in table_data if all(row.get(k) == v for k, v in where_clause.items())]
    else:
        result = table_data

    if not result:
        print("Записей не найдено.")
        return

    # Вывод через PrettyTable
    table = PrettyTable()
    table.field_names = list(result[0].keys())
    for row in result:
        table.add_row([row[col] for col in table.field_names])
    print(table)

def update(table_data, set_clause, where_clause):
    """Обновляет записи по условию."""
    updated_count = 0
    for row in table_data:
        if all(row.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                row[k] = v
            updated_count += 1
    save_table_data(set_clause.get("table_name"), table_data)
    print(f"{updated_count} записей успешно обновлено.")

def delete(table_data, where_clause):
    """Удаляет записи по условию."""
    initial_len = len(table_data)
    table_data[:] = [row for row in table_data if not all(row.get(k) == v for k, v in where_clause.items())]
    deleted_count = initial_len - len(table_data)
    save_table_data(where_clause.get("table_name"), table_data)
    print(f"{deleted_count} записей успешно удалено.")

