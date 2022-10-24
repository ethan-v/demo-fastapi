from sqlalchemy import desc

from vinor.builder.base.base_repository import BaseRepository
from .builder_data_table import BuilderDataTable
from ..database import BuilderDBModel


class BuilderDataRepository(BaseRepository):

    table = BuilderDataTable

    def find_by_field_and_table(self, table_name: str, field_name: str):
        return self.db.query(self.table).filter(self.table.schema_name == table_name, self.table.field_name == field_name).first()

    def find_by_table(self, table_name: str):
        return self.db.query(self.table).filter(self.table.table_name == table_name).all()

    def latest(self, table_name: str):
        return self.db.query(self.table)\
            .filter(self.table.schema_name == table_name)\
            .order_by(desc('field_id'))\
            .first()
