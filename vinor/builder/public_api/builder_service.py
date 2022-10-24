from faker import Faker
from sqlalchemy.orm import Session

from vinor.builder.base.base_response import PaginationResponse
from vinor.builder.bdata.builder_data_models import BuilderDataCreate, BuilderDataResponse
from vinor.builder.bdata.builder_data_repository import BuilderDataRepository
from vinor.builder.bdata.builder_data_table import BuilderDataTable
from vinor.builder.field.builder_field_repository import BuilderFieldRepository
from vinor.builder.schema.builder_schema_repository import BuilderSchemaRepository

faker = Faker()


class BuilderService:
    db: Session = NotImplementedError

    def __init__(self, db):
        self.db = db

    def load_resource(self, table_name: str, view: str):
        table = BuilderSchemaRepository(self.db).find_by_name(name=table_name)
        columns = BuilderFieldRepository(self.db).find_by_table(table_name=table_name)

        # Format as: field = value
        detail_item = {}
        list_items = []

        for column in columns:
            value = "Faked"

            print("column.data_type: " + column.name)

            # Check datatype
            if column.data_type == 'int':
                value = faker.random_number()
            elif column.data_type == 'str':
                value = faker.text(20)

            # Check specific column name: slug
            if column.name == 'slug':
                value = faker.slug()

            # column_data = BuilderDataRepository(self.db).find_by_field_and_table(table_name=table.name, field_name=column.name)
            # print(f"table_name={table.name}, field_name={column.name}")
            # print(column_data.id)

            column_data = BuilderDataRepository(self.db).find_by_field_and_table(table_name='course', field_name=column.name)
            print(f"================ column_data.id: {column_data}")
            # if ()
            # break

            # obj = BuilderDataResponse(**column_data)
            # print(obj)

            value = column_data.data if column_data is not None else None

            detail_item[column.name] = value

        list_items.append(detail_item)

        # Format for: view=list
        if view == 'detail':
            return detail_item
        elif view == 'list':
            items = []
            # for i in range(1, 25):
            #     new_item = detail_item.copy()
            #     new_item['id'] = i
            #     items.append(new_item)

            return PaginationResponse(
                total=len(list_items),
                limit=10,
                skip=0,
                total_page=2,
                next_page_link=None,
                items=list_items
            )

    def create_resource_data(self, table_name: str, data: dict):
        # return data
        debug_obj = []
        latest = BuilderDataRepository(self.db).latest(table_name=table_name)
        latest_field_id = latest.id + 1 if latest is not None else 1
        response_obj = {}
        for field_name, value in data.items():
            obj = BuilderDataCreate(
                schema_name=table_name,
                field_id=latest_field_id,
                field_name=field_name,
                data=value,
            )
            record = BuilderDataRepository(self.db).create(data=obj)
            debug_obj.append(obj)
            response_obj[field_name] = value

        return response_obj
        # return record
        # return {
        #     "title": "Full age become.",
        #     "slug": "read-suddenly",
        #     "image": "https://www.python.org/static/community_logos/python-powered-w-100x40.png",
        #     "description": "Job above condition.",
        #     "content": "Ball huge mean.",
        #     "price": "Faked",
        #     "course_category": 544217514
        # }
