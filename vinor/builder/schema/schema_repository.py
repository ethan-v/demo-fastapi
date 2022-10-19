from vinor.builder.base.base_repository import BaseRepository
from .schema_table import SchemaTable


class SchemaRepository(BaseRepository):

    table = SchemaTable

    def find_by_name(self, name: str):
        return self.db.query(self.table).filter(self.table.name == name).first()
