from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.menu import Menu


class MenuRepository(BaseRepository):

    model = Menu

    def find_by_title(self, title: str):
        return self.db.query(self.model).filter(self.model.title == title).first()

    def find_by_url(self, url: str):
        return self.db.query(self.model).filter(self.model.url == url).first()
