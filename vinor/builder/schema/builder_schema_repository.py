from vinor.builder.base.base_repository import BaseRepository
from .builder_schema_table import BuilderSchemaTable


class BuilderSchemaRepository(BaseRepository):

    table = BuilderSchemaTable

    def find_by_name(self, name: str):
        return self.db.query(self.table).filter(self.table.name == name).first()
