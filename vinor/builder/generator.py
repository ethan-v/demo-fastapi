from vinor.builder.field.builder_field_models import BuilderFieldBase
from vinor.builder.schema.builder_schema_models import BuilderSchemaBase


def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


example_response_json = {
    "course": {
        "id": 1,
        "title": "Python for Back-end Engineer",
        "slug": "python-for-backend-engineer",
        "image": "https://www.python.org/static/img/python-logo.png",
        "description": "Python background job, script, asynchronous",
        "content": "Python background job, script, asynchronous",
        "price": 4.99,
        "course_category": 1,
    },
    "course_lecture": {
        "id": 1,
        "title": "Basic data type in Python",
        "slug": "basic-data-type-in-python",
    },
    "course_video": {
        "id": 1,
        "course_id": 1,
        "lecture_id": 1,
    }
}


def convert_value_to_datatype(value):
    return type(value).__name__


class Generator:
    example_json: dict

    def set_example_json_data(self, example_json: dict):
        self.example_json = example_json

    def generate(self):
        schemas = []
        for schema_name, item in self.example_json.items():
            # print(f"Table name: {schema_name}, example data: {item}")
            table_fields = []
            for field_name, field_value in item.items():
                table_fields.append(BuilderFieldBase(
                    name=field_name,
                    schema_name=schema_name,
                    data_type=convert_value_to_datatype(field_value),
                    default=None,
                    relation_mapping=None,
                    comment=None,
                    is_required=True,
                    in_request=True,
                    in_request_name=None,
                    in_response=True,
                    in_response_name=None,
                    callback_function=None,
                    created_at=None,
                    updated_at=None,
                ))

            schemas.append(BuilderSchemaBase(
                name=schema_name.lower(),
                is_active=False,
                fields=table_fields,
            ))
            break
        return schemas


if __name__ == '__main__':
    generator = Generator()
    generator.set_example_json_data(example_response_json)
    schemas = generator.generate()
    print(schemas)
