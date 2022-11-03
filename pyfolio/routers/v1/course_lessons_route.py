from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pyfolio.dependencies import get_db
from pyfolio.repositories.course_lesson_repository import CourseLessonRepository
from pyfolio.schemas.base_response_schema import SuccessResponse
from pyfolio.schemas.course_lesson_schema import CourseLessonCreate, CourseLessonUpdate

router = APIRouter()


@router.get("")
def read_lessons(skip: int = 0, limit: int = 10, sort: str = 'id', order='desc',
               search_by: str = '', search_value: str = '',
               db: Session = Depends(get_db)):
    lessons =CourseLessonRepository(db).paginate(
        skip=skip,
        limit=limit,
        sort=sort,
        order=order,
        search_by=search_by,
        search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve lessons successfully',
        data=lessons
    )


@router.get("/{id}")
def read_lesson(id: int, db: Session = Depends(get_db)):
    lesson =CourseLessonRepository(db).find(id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return SuccessResponse(
        message='Retrieve lesson successfully',
        data=lesson
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_lesson(lesson:CourseLessonCreate, db: Session = Depends(get_db)):
    db_lesson =CourseLessonRepository(db).find_by_title(lesson.title)
    if db_lesson:
        raise HTTPException(status_code=400, detail="Title already exists")
    lesson =CourseLessonRepository(db).create(lesson)
    if lesson is None:
        raise HTTPException(status_code=500, detail="Failed to create lesson")
    else:
        return SuccessResponse(
            message='Created lesson',
            data=lesson
        )


@router.put("/{id}")
def update_lesson(id: int, lesson:CourseLessonUpdate, db: Session = Depends(get_db)):
    db_lesson =CourseLessonRepository(db).find(id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    lesson_data = lesson.dict(exclude_unset=True)
    print(lesson_data)
    for key, value in lesson_data.items():
        setattr(db_lesson, key, value)
    lesson =CourseLessonRepository(db).update(db_lesson)
    return SuccessResponse(
        message='Updated lesson',
        data=lesson
    )


@router.delete("/{id}")
def delete_lesson(id: int, db: Session = Depends(get_db)):
    db_lesson =CourseLessonRepository(db).find(id)
    if db_lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    CourseLessonRepository(db).delete(db_lesson)
    return {
        "message": "Lesson was deleted successfully."
    }
