from pyfolio.apps.builder.base.base_repository import BaseRepository
from .builder_field_models import BuilderFieldBase
from .builder_field_table import BuilderFieldTable
from ..generator import convert_value_to_datatype


class BuilderFieldRepository(BaseRepository):

    table = BuilderFieldTable

    def find_by_name_and_schema(self, schema_name: str, name: str):
        return self.db.query(self.table).filter(self.table.schema_name == schema_name, self.table.name == name).first()

    def get_by_table(self, table_name: str):
        return self.db.query(self.table).filter(self.table.schema_name == table_name).all()

    def create_fields_from_sample(self, schema_name: str, data: dict) -> list:
        created_fields = []
        for field_name, field_value in data.items():
            field = BuilderFieldBase(
                name=field_name,
                schema_name=schema_name,
                data_type=convert_value_to_datatype(field_value),
                default=None,
                relation_mapping=None,
                comment=None,
                is_required=True,
                in_request=True,
                in_request_name=None,
                in_response=True,
                in_response_name=None,
                callback_function=None,
                created_at=None,
                updated_at=None,
            )
            found_field = self.find_by_name_and_schema(schema_name=schema_name, name=field_name)
            if found_field is None:
                created_field = self.create(field)
                field_output = field.dict()
                field_output['id'] = created_field.id
                created_fields.append(field_output)
            else:
                created_fields.append(dict(found_field.__dict__))
        return created_fields
