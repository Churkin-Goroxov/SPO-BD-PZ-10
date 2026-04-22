import re
import csv
from typing import List, Dict, Any


class SQLTable:
    def __init__(self,
                 db_config: Dict[str, Any],
                 table_name: str,
                 pk: str = "id",
                 db_type: str = "postgres"):
        if db_type not in ("postgres", "mysql"):
            raise ValueError("db_type must be 'postgres' or 'mysql'")
        self.db_type = db_type

        self.db_config = db_config
        self._validate_name(table_name)
        self._validate_name(pk)

        self.table_name = table_name
        self.pk = pk

        if self.db_type == "postgres":
            import psycopg2
            self.connection = psycopg2.connect(**db_config)
        elif self.db_type == "mysql":
            import mysql.connector
            self.connection = mysql.connector.connect(**db_config)

        self.cursor = self.connection.cursor()

        # для query builder
        self._select = []
        self._where = []
        self._join = []

    @staticmethod
    def _validate_name(name: str) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_]+", name):
            raise ValueError(f"Недопустимое имя: {name}")

    # UNIVERSAL FORGING TOOLS
    def _q(self, name: str) -> str:
        self._validate_name(name)
        if self.db_type == "postgres":
            return f'"{name}"'
        else:
            return f'`{name}`'

    def _format_column(self, col: str) -> str:
        if "." in col:
            table, field = col.split(".")
            self._validate_name(table)
            self._validate_name(field)
            return f'{self._q(table)}.{self._q(field)}'
        else:
            self._validate_name(col)
            return self._q(col)

    #  TABLE
    def create_table(self, columns: list, primary_key=None):
        parts = []
        auto_incr = None

        for column in columns:
            name = column["name"]
            col_type = column["type"]

            self._validate_name(name)

            if column.get("auto_increment", False):
                if self.db_type == "postgres":
                    col_def = f'{self._q(name)} SERIAL PRIMARY KEY'
                    auto_incr = None
                else:
                    col_def = f'{self._q(name)} INT AUTO_INCREMENT'
                    auto_incr = name
            else:
                col_def = f'{self._q(name)} {col_type}'

            if not column.get("nullable", True):
                col_def += " NOT NULL"

            if column.get("unique", False):
                col_def += " UNIQUE"

            if "default" in column:
                default = column["default"]
                if isinstance(default, str):
                    safe = default.replace("'", "''")
                    col_def += f" DEFAULT '{safe}'"
                else:
                    col_def += f" DEFAULT {default}"

            parts.append(col_def)

        if auto_incr:
            parts.append(f'PRIMARY KEY ({self._q(auto_incr)})')
        elif primary_key:
            self._validate_name(primary_key)
            parts.append(f'PRIMARY KEY ({self._q(primary_key)})')

        body = ",\n ".join(parts)

        query = f'''
        CREATE TABLE IF NOT EXISTS {self._q(self.table_name)} (
        {body}
        );
        '''

        self.cursor.execute(query)
        self.connection.commit()

    #  SELECT
    def get_all(self):
        self.cursor.execute(f'SELECT * FROM {self._q(self.table_name)}')
        return self.cursor.fetchall()

    def get_by_id(self, value: int):
        self.cursor.execute(
            f'SELECT * FROM {self._q(self.table_name)} WHERE {self._q(self.pk)} = %s',
            (value,)
        )
        return self.cursor.fetchone()

    def get_value(self, column_name: str, value: Any):
        self._validate_name(column_name)
        self.cursor.execute(
            f'SELECT * FROM {self._q(self.table_name)} WHERE {self._q(column_name)} = %s',
            (value,)
        )
        return self.cursor.fetchall()

    #  INSERT
    def insert(self, data: Dict[str, Any]):
        columns = list(data.keys())

        for col in columns:
            self._validate_name(col)

        columns_str = ", ".join(self._q(col) for col in columns)
        placeholders = ", ".join(["%s"] * len(columns))
        values = tuple(data.values())

        query = f'INSERT INTO {self._q(self.table_name)} ({columns_str}) VALUES ({placeholders})'
        self.cursor.execute(query, values)
        self.connection.commit()

    def insert_many(self, data_list: List[Dict[str, Any]]):
        if not data_list:
            return

        columns = list(data_list[0].keys())

        for col in columns:
            self._validate_name(col)

        for row in data_list:
            if list(row.keys()) != columns:
                raise ValueError("Все словари должны иметь одинаковые ключи")

        columns_str = ", ".join(f'{self._q(col)}' for col in columns)
        placeholders = ", ".join(["%s"] * len(columns))
        values = [tuple(row[col] for col in columns) for row in data_list]

        query = f'INSERT INTO {self._q(self.table_name)} ({columns_str}) VALUES ({placeholders})'
        self.cursor.executemany(query, values)
        self.connection.commit()

    #  UPDATE
    def update(self, value: int, data: Dict[str, Any]):
        for col in data.keys():
            self._validate_name(col)

        set_values = ", ".join(f'{self._q(k)} = %s' for k in data.keys())
        values = tuple(data.values()) + (value,)

        query = f'UPDATE {self._q(self.table_name)} SET {set_values} WHERE {self._q(self.pk)} = %s'
        self.cursor.execute(query, values)
        self.connection.commit()

    #  DELETE
    def delete_by_id(self, value: int):
        self.cursor.execute(
            f'DELETE FROM {self._q(self.table_name)} WHERE {self._q(self.pk)} = %s',
            (value,)
        )
        self.connection.commit()

    def delete_table(self):
        if self.db_type == "postgres":
            query = f'DROP TABLE IF EXISTS {self._q(self.table_name)} CASCADE'
        else:
            query = f'DROP TABLE IF EXISTS {self._q(self.table_name)}'

        self.cursor.execute(query)
        self.connection.commit()

    #  JOIN
    def inner_join(self, other_table: str, left: str, right: str):
        self._join.append(f'INNER JOIN {self._q(other_table)} ON'
                          f' {self._format_column(left)} = {self._format_column(right)}')
        return self

    def left_join(self, other_table: str, left: str, right: str):
        self._join.append(f'LEFT JOIN {self._q(other_table)} ON '
                          f'{self._format_column(left)} = {self._format_column(right)}')
        return self

    #  UNION
    def union(self, other_query: str):
        return f"({self.build_query()}) UNION ({other_query})"

    #  QUERY BUILDER
    def select(self, *columns):
        self._select = columns
        return self

    def where(self, condition: str):
        self._where.append(condition)
        return self

    def build_query(self):
        columns = ", ".join(self._format_column(c) for c in self._select) if self._select else "*"
        query = f'SELECT {columns} FROM {self._q(self.table_name)}'

        if self._join:
            query += " " + " ".join(self._join)

        if self._where:
            query += " WHERE " + " AND ".join(self._where)

        return query

    def execute(self):
        query = self.build_query()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    #  CSV
    def export_csv(self, filename: str):
        self.cursor.execute(f'SELECT * FROM {self._q(self.table_name)}')
        headers = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def import_csv(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                raise ValueError("CSV без заголовков")

            for col in reader.fieldnames:
                self._validate_name(col)

            self.insert_many(list(reader))

    #  CLOSE
    def close(self):
        self.cursor.close()
        self.connection.close()


# КОНФИГИ
db_config_pg = {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "user",
    "password": "1234",
    "dbname": "mybd"
}

db_config_mysql = {
    "host": "localhost",
    "user": "admin",
    "password": "admin",
    "database": "new_schema",
    "use_pure": True,
    "port": 3306
}

"""
фичи:
  добавлен lazy import
  валидация данныъ от SQL-инъекций
  
"""
