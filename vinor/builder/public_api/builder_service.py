from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from vinor.builder.bdata.builder_data_models import BuilderDataCreate
from vinor.builder.bdata.builder_data_repository import BuilderDataRepository
from vinor.builder.field.builder_field_repository import BuilderFieldRepository

faker = Faker()


class BuilderService:
    db: Session = NotImplementedError

    def __init__(self, db):
        self.db = db

    def load_resource_data_as_list(self, table_name: str):
        columns = BuilderFieldRepository(self.db).get_by_table(table_name=table_name)
        column_values = BuilderDataRepository(self.db).get_by_table(table_name=table_name)
        map_items = {}
        map_columns = {}

        for col in columns:
            if col.name not in map_columns:
                map_columns[col.name] = col

        for value in column_values:
            id = value.field_id
            field_name = value.field_name
            field_value = value.data

            # Check column data type
            if field_name != 'id':
                column = map_columns[field_name]
                if column.data_type == 'int':
                    field_value = int(field_value)
                elif column.data_type == 'float':
                    field_value = float(field_value)
                elif column.data_type == 'bool':
                    field_value = bool(field_value)

            # Build item object
            if id not in map_items:
                map_items[id] = {"id": id}
            if field_name not in map_items[id]:
                map_items[id][field_name] = field_value
        return list(map_items.values())

    def load_resource_data_as_detail(self, table_name: str, field_id: int):
        columns = BuilderFieldRepository(self.db).get_by_table(table_name=table_name)
        column_values = BuilderDataRepository(self.db).get_by_field_id(table_name=table_name, field_id=field_id)

        if len(column_values) == 0:
            return None

        single_item = {}
        map_columns = {}

        for col in columns:
            if col.name not in map_columns:
                map_columns[col.name] = col

        for value in column_values:
            id = value.field_id
            field_name = value.field_name
            field_value = value.data

            # Check column data type
            if field_name != 'id':
                column = map_columns[field_name]
                if column.data_type == 'int':
                    field_value = int(field_value)
                elif column.data_type == 'float':
                    field_value = float(field_value)
                elif column.data_type == 'bool':
                    field_value = bool(field_value)

            # Build item object
            if "id" not in single_item:
                single_item["id"] = id

            if field_name not in single_item:
                single_item[field_name] = field_value

        return single_item

    def create_resource_data(self, table_name: str, data: dict):
        latest = BuilderDataRepository(self.db).latest(table_name=table_name)
        latest_field_id = latest.field_id + 1 if latest is not None else 1
        response_obj = {
            "id": latest_field_id
        }
        for field_name, value in data.items():
            obj = BuilderDataCreate(
                schema_name=table_name,
                field_id=latest_field_id,
                field_name=field_name,
                data=value,
            )
            BuilderDataRepository(self.db).create(data=obj)
            response_obj[field_name] = value
        return response_obj

    def update_resource_data(self, table_name: str, field_id: int, data: dict):
        column_values = BuilderDataRepository(self.db).get_by_field_id(table_name=table_name, field_id=field_id)
        print(f"======= update_resource_data =====================")
        print("column_values")
        print(column_values)
        try:
            for item in column_values:
                field_name = item.field_name
                # print(f"In Database: {item.field_name}={item.data}")
                # item.data = "new data"
                # print(f"In Database: {item.field_name}={item.data}")
                if field_name in data:
                    item.data = data[field_name]
                BuilderDataRepository(self.db).update(db_table=item)
            return self.load_resource_data_as_detail(table_name=table_name, field_id=field_id)
        except SQLAlchemyError:
            return None
