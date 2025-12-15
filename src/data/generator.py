from typing import List, Dict, Any
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    JSON,
    Enum,
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql
from .schema import TableSchema, DataType


class SchemaGenerator:
    def __init__(self):
        self.metadata = MetaData()
        self.type_mapping = {
            DataType.INTEGER: Integer,
            DataType.STRING: String(255),
            DataType.BOOLEAN: Boolean,
            DataType.FLOAT: Float,
            DataType.TIMESTAMP: DateTime,
            DataType.JSON: JSON,
        }

    def create_table_from_schema(self, schema: TableSchema) -> Table:
        columns = []
        for col_def in schema.columns:
            if col_def.data_type == DataType.ENUM:
                if not col_def.enum_values:
                    raise ValueError(
                        f"Column {col_def.name} is of type ENUM but has no enum_values defined"
                    )
                # For SQLAlchemy Enum, we need to pass the allowed values
                # We also set the name of the enum type to avoid conflicts
                enum_name = (
                    col_def.enum_name
                    if col_def.enum_name
                    else f"{schema.name}_{col_def.name}_enum"
                )
                col_type = Enum(*col_def.enum_values, name=enum_name)
            else:
                col_type = self.type_mapping[col_def.data_type]

            # Construct column arguments
            col_args: Dict[str, Any] = {
                "primary_key": col_def.primary_key,
                "nullable": col_def.nullable,
                "unique": col_def.unique,
            }

            if col_def.default is not None:
                col_args["server_default"] = col_def.default

            column = Column(col_def.name, col_type, **col_args)
            columns.append(column)

        return Table(schema.name, self.metadata, *columns)

    def generate_ddl(self, tables: List[TableSchema]) -> str:
        """Generates SQL DDL for a list of table schemas."""
        ddl_statements = []
        for table_schema in tables:
            sa_table = self.create_table_from_schema(table_schema)
            # Use MySQL dialect as Dolt is MySQL compatible
            create_stmt = CreateTable(sa_table).compile(dialect=mysql.dialect())
            ddl_statements.append(str(create_stmt).strip() + ";")

        return "\n\n".join(ddl_statements)
