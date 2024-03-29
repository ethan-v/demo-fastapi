from pyfolio.apps.builder.database import init_db
from pyfolio.apps.builder.schema.builder_schema_table import BuilderSchemaTable
from pyfolio.apps.builder.configs import BuilderConfig


class Builder:

    settings: BuilderConfig
    schema: BuilderSchemaTable
    embedded_app_name: str
    embedded_app_configs: dict

    def __init__(self, embedded_app_name: str, embedded_app_configs: dict):
        self.settings = BuilderConfig()
        self.embedded_app_name = embedded_app_name
        self.embedded_app_configs = embedded_app_configs

    def load(self):
        print("[BUILDER] Settings: {}".format(self.settings))
        print("[BUILDER] Embedded app name: {}".format(self.embedded_app_name))
        print("[BUILDER] Embedded app configs: {}".format(self.embedded_app_configs))
        init_db()
        print("[BUILDER] Builder application initialize complete.")


def init_builder(embedded_app_name: str, embedded_app_configs: dict):
    builder = Builder(embedded_app_name=embedded_app_name, embedded_app_configs=embedded_app_configs)
    builder.load()
