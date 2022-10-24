from vinor.builder.base.base_repository import BaseRepository
from .builder_field_table import BuilderFieldTable


class BuilderFieldRepository(BaseRepository):

    table = BuilderFieldTable

    def find_by_name_and_schema(self, schema_name: str, name: str):
        return self.db.query(self.table).filter(self.table.schema_name == schema_name, self.table.name == name).first()

    def get_by_table(self, table_name: str):
        return self.db.query(self.table).filter(self.table.schema_name == table_name).all()
