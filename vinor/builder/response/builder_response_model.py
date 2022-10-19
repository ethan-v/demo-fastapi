from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from vinor.builder.database import BuilderDBModel


class BuilderResponse(BuilderDBModel):
    """
        Builder responses table
        - name:
            Eg: course_list | course_detail | user->course_list
        - field_mapping:
            Eg:
                {
                    "name": "name",
                    "record_file": "record_file",
                    "content": "content",
                    "record_file_url": "callback_function_getPublicUrl"
                }
    """
    __tablename__ = "builder_responses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    field_mapping = Column(String(1000))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
