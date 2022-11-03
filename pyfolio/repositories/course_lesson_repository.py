from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.course_lesson import CourseLesson


class CourseLessonRepository(BaseRepository):

    model = CourseLesson

    def find_by_title(self, title: str):
        return self.db.query(self.model).filter(self.model.title == title).first()
