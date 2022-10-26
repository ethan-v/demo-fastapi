from sqlalchemy import desc
from vinor.builder.base.base_repository import BaseRepository
from vinor.builder.bdata.builder_data_table import BuilderDataTable


class BuilderDataRepository(BaseRepository):
    table = BuilderDataTable

    def find_by_field_and_table(self, table_name: str, field_name: str):
        return self.db.query(self.table).filter(
            self.table.schema_name == table_name,
            self.table.field_name == field_name
        ).first()

    def find_by_field_id(self, table_name: str, field_id: str):
        return self.db.query(self.table).filter(
            self.table.schema_name == table_name,
            self.table.field_id == field_id
        ).first()

    def get_by_table(self, table_name: str, skip: int = 0, limit: int = 10, order_by: str = ''):
        return self.db.query(self.table)\
            .filter(self.table.schema_name == table_name)\
            .offset(skip).limit(limit)\
            .all()

    def count_by_table(self, table_name: str):
        return self.db.query(self.table).filter(self.table.schema_name == table_name).count()

    def get_by_field_id(self, table_name: str, field_id: int):
        return self.db.query(self.table).filter(self.table.schema_name == table_name,
                                                self.table.field_id == field_id).all()

    def latest(self, table_name: str):
        return self.db.query(self.table) \
            .filter(self.table.schema_name == table_name) \
            .order_by(desc('field_id')) \
            .first()

    def delete_by_field_id(self, table_name: str, field_id: int):
        records = self.db.query(self.table).filter(self.table.schema_name == table_name,
                                                   self.table.field_id == field_id).all()
        for record in records:
            self.delete(record)
        return None
