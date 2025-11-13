import json
import os

DB_DIR = "data"

def ensure_data_dir():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

def load_metadata(filepath="db_meta.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath="db_meta.json", data=None):
    data = data or {}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    ensure_data_dir()
    path = os.path.join(DB_DIR, f"{table_name}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    ensure_data_dir()
    path = os.path.join(DB_DIR, f"{table_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


