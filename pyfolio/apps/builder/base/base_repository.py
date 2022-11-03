
import abc
import inspect
import math
from sqlalchemy.orm import Session
from sqlalchemy import desc

from pyfolio.apps.builder.database import BuilderDBModel
from pyfolio.apps.builder.base.base_response import PaginationResponse


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def to_dict(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, obj):
        raise NotImplementedError


class BaseRepository(AbstractRepository):

    table: object = NotImplementedError
    db: Session = NotImplementedError

    def __init__(self, db: Session):
        self.db = db

    def to_dict(self, obj):
        if obj is not None:
            return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
        else:
            return {}

    def to_list(self, _list):
        if isinstance(_list, list) and len(_list):
            output = []
            for item in _list:
                output.append(self.to_dict(item))
            return output
        else:
            print("A list is reuired!")
            return []

    def _is_empty(self, value):
        if value is None:
            return True
        elif isinstance(value, str) and value.strip() == '':
            return True
        return False

    def get(self, skip: int = 0, limit: int = 10):
        return self.db.query(self.table).offset(skip).limit(limit).all()

    def find_by_field(self, field: str, value):
        return self.db.query(self.table).filter(self.table[field] == value).first()

    def find(self, id: int):
        return self.db.query(self.table).filter(self.table.id == id).first()

    def create(self, data: BuilderDBModel):
        obj = self.table(**data.dict())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, db_table: BuilderDBModel):
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return db_table

    def delete(self, db_table: BuilderDBModel):
        self.db.delete(db_table)
        self.db.commit()

    def paginate(self, limit: int = 10, skip: int = 0,
            order_by: str = 'id', order_direct='desc',
            search_by: str = '', search_value: str = ''):

        search_by = search_by.strip()
        search_value = search_value.strip()
        next_page = None
        data = []

        if order_direct == 'desc':
            order_by = desc(order_by)

        # Create query
        query = self.db.query(self.table).order_by(order_by)

        # Search by title or dynamic field
        if search_by == 'title' and hasattr(self.table, 'title'):
            query = query.where(self.table.title.like(f'%{search_value}%'))
        if search_by == 'email' and hasattr(self.table, 'email'):
            query = query.where(self.table.email.like(f'%{search_value}%'))
        # elif hasattr(self.table, search_by):
        #     query = query.where(self.table[search_by].like(f'%{search_value}%'))

        # Count total records
        total = query.count()
        total_page = math.ceil(total / limit) if total > 0 else 0

        # Limit & offset
        if total > 0:
            query = query.offset(skip).limit(limit)
            data = list(query)
            if len(data) > 0:
                last = data[-1]
                next_page = f'?limit={limit}&offset={last.id}&search_by={search_by}&search_value={search_value}'

        return PaginationResponse(
            total=total,
            limit=limit,
            offset=skip,
            total_page=total_page,
            next_page_link=next_page,
            items=data
        )
