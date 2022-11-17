import json
import os
import sqlalchemy
from sqlalchemy import Table
from typing import List
from pyfolio.models.db import engine, DBModel


class DBCliHelper:

    def check_table_exist(self, table_name: str):
        return sqlalchemy.inspect(engine).has_table(table_name)

    def insert_many(self, table_name: str, items: List[dict]):
        DBModel.metadata.reflect(engine, only=[table_name])
        table = Table(table_name, DBModel.metadata)
        with engine.connect() as conn:
            conn.execute(table.insert().prefix_with('IGNORE'), items)

    def import_from_json(self, file_path: str):
        file = open(file_path)
        items = json.load(file)
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        print("=================================")
        print("table name: " + table_name)
        print(items)

        if not self.check_table_exist(table_name):
            return f"Not found table: {table_name}!"
        else:
            # for item in items:
            self.insert_many(table_name=table_name, items=items)
            return None
