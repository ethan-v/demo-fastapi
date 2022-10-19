from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from vinor.builder.database import BuilderDBModel


class BuilderField(BuilderDBModel):
    """
        Builder fields table
        - name:
            Eg: audio_file
        - data_type:
            Eg: string | integer | float | boolean | file | file_image
        - default:
            Eg: null or "" or 0 or false
        - relation_mapping:
            Eg1: (2 schemas) One Category has many posts:
                {field_name: "id", relation_schema:"posts", relation_field: "category_id", relation_type: "one_to_many"}
            Eg2: (2 schemas) Many posts in one category:
                {field_name: "category_id", relation_schema:"categories", relation_field: "id", relation_type: "many_to_one"}
            Eg3: (3 schemas) Many posts has many tags:
                {field_name: "post_id,tag_id", relation_schema:"tags", relation_field: "id", relation_type: "many_to_many"}
        - comment:
            Eg: Audio file url
        - is_required
            Eg: true or false
        - in_request
            Eg: True
        in_request_name:
            Eg: (a custom name) my_file
        - in_response:
            Eg: False
        - in_response_name:
            Eg: (a custom name) audio_link
    """
    __tablename__ = "builder_fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    data_type = Column(String(255))
    default = Column(String(255), default=None)
    relation_mapping = Column(String(255), default=None)
    comment = Column(String(255), default=None)
    is_required = Column(Boolean, default=False)
    in_request = Column(Boolean, default=True)
    in_request_name = Column(String(255), default=None)
    in_response = Column(Boolean, default=True)
    in_response_name = Column(String(255), default=None)
    callback_function = Column(String(255), default=None)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
