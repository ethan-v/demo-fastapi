from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.page import Page


class PageRepository(BaseRepository):

    model = Page

    def find_by_title(self, title: str):
        return self.db.query(self.model).filter(self.model.title == title).first()

    def find_by_slug(self, slug: str):
        return self.db.query(self.model).filter(self.model.slug == slug).first()
