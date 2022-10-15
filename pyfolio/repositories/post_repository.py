from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.post import Post


class PostRepository(BaseRepository):

    model = Post

    def find_by_title(self, title: str):
        return self.db.query(self.model).filter(self.model.title == title).first()
