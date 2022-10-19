from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from vinor.builder.database import BuilderDBModel


class BuilderRequest(BuilderDBModel):
    """
        Builder requests table
        - sample_payload:
            Eg: {
                    name: "Introduction your self for the interview",
                    content: "Hi, I'm Ethan. I'm A Software Engineer. ...",
                    record_file: "/static/audios/record_123.mp3"
                }
        - field_mapping:
            Eg:
                {
                    "name": "name",
                    "file": "record_file",
                    "content": "content"
                }
    """
    __tablename__ = "builder_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    sample_payload = Column(String(1000))
    field_mapping = Column(String(1000))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
