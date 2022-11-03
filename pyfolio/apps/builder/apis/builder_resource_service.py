import json
import math

from faker import Faker
from sqlalchemy import desc
from sqlalchemy.orm import Session

from pyfolio.apps.builder.base.base_response import PaginationResponse
from pyfolio.apps.builder.bdata.builder_data_models import BuilderDataCreate
from pyfolio.apps.builder.bdata.builder_data_repository import BuilderDataRepository
from pyfolio.apps.builder.field.builder_field_repository import BuilderFieldRepository

faker = Faker()


class BuilderService:
    db: Session = NotImplementedError

    def __init__(self, db):
        self.db = db

    def load_resource_data_as_list(self, table_name: str, limit: int = 10,
                       skip: int = 0, sort: str = 'field_id', order='desc'):
        next_page = None
        items = []
        total = BuilderDataRepository(self.db).count_by_table(table_name=table_name)
        total_page = math.ceil(total / limit) if total > 0 else 0

        if order == 'desc':
            order_by = desc(sort)

        # Limit & offset
        if total > 0:
            query = BuilderDataRepository(self.db).get_by_table(
                table_name=table_name,
                skip=skip,
                limit=limit,
                order_by=order_by
            )
            records = list(query)
            if len(records) > 0:
                last = records[-1]
                next_page = f'?limit={limit}&offset={last.id}&search_by=&search_value='

                for record in records:
                    data = json.loads(record.data)
                    data['id'] = record.field_id
                    items.append(data)

        return PaginationResponse(
            total=total,
            limit=limit,
            offset=skip,
            total_page=total_page,
            next_page_link=next_page,
            items=items
        )

    def load_resource_data_as_detail(self, table_name: str, field_id: int):
        record = BuilderDataRepository(self.db).find_by_field_id(table_name=table_name, field_id=field_id)
        if record is not None and record.data is not None:
            data = json.loads(record.data)
            data['id'] = record.field_id
            return data
        return {}

    def create_resource_data(self, table_name: str, data: dict):
        latest = BuilderDataRepository(self.db).latest(table_name=table_name)
        latest_field_id = latest.field_id + 1 if latest is not None else 1
        columns = BuilderFieldRepository(self.db).get_by_table(table_name=table_name)
        create_obj = {}

        for col in columns:
            field_name = col.name
            print(f"field_name: {field_name}")
            if field_name not in create_obj:
                create_obj[field_name] = None
            if field_name in data:
                create_obj[field_name] = data[field_name]

        obj = BuilderDataCreate(
            schema_name=table_name,
            field_id=latest_field_id,
            field_name="",
            data=json.dumps(create_obj),
        )

        record = BuilderDataRepository(self.db).create(data=obj)
        detail = json.loads(record.data)
        detail['id'] = record.field_id
        return detail

    def update_resource_data(self, table_name: str, field_id: int, data: dict):
        record = BuilderDataRepository(self.db).find_by_field_id(table_name=table_name, field_id=field_id)
        if record is not None:
            columns = BuilderFieldRepository(self.db).get_by_table(table_name=table_name)
            data_update = json.loads(record.data)

            for col in columns:
                field_name = col.name
                if field_name in data_update and field_name in data:
                    data_update[field_name] = data[field_name]

            record.data = json.dumps(data_update)
            updated_record = BuilderDataRepository(self.db).update(record)

            detail = json.loads(updated_record.data)
            detail['id'] = record.id
            return detail
        return None

    def delete_resource_data(self, table_name: str, field_id: int):
        return BuilderDataRepository(self.db).delete_by_field_id(table_name=table_name, field_id=field_id)
