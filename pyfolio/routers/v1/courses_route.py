from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from pyfolio.repositories.course_repository import CourseRepository
from pyfolio.dependencies import get_db
from pyfolio.schemas.course_schema import CourseCreate, CourseUpdate
from pyfolio.schemas.base_response_schema import SuccessResponse


router = APIRouter()


@router.get("")
def read_courses(
    skip: int = 0, limit: int = 10, sort: str = 'id', order='desc', search_by: str = '', search_value: str = '',
    db: Session = Depends(get_db)
):
    courses = CourseRepository(db).paginate(
        skip=skip, limit=limit,
        sort=sort, order=order,
        search_by=search_by, search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve car brands successfully',
        data=courses
    )


@router.get("/{id}")
def read_course(id: int, db: Session = Depends(get_db)):
    course = CourseRepository(db).find(id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return SuccessResponse(
        message='Retrieve car brand successfully',
        data=course
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = CourseRepository(db).find_by_title(course.title)
    if db_course:
        raise HTTPException(status_code=400, detail="Name already exists")
    course = CourseRepository(db).create(course)
    if course is None:
        raise HTTPException(status_code=500, detail="Failed to create Course")
    else:
        return SuccessResponse(
            message='Created Course',
            data=course,
        )


@router.put("/{id}")
def update_course(id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = CourseRepository(db).find(id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course_data = course.dict(exclude_unset=True)
    for key, value in course_data.items():
        setattr(db_course, key, value)
    course = CourseRepository(db).update(db_course)
    return SuccessResponse(
        message='Updated Course',
        data=course,
    )


@router.delete("/{id}")
def delete_course(id: int, db: Session = Depends(get_db)):
    db_course = CourseRepository(db).find(id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    CourseRepository(db).delete(db_course)
    return {
        "message": "Course was deleted successfully."
    }
