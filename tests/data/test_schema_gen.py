from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.generator import SchemaGenerator
import pytest


def test_generate_simple_table_ddl():
    table = TableSchema(
        name="users",
        description=None,
        columns=[
            ColumnSchema(
                name="id",
                data_type=DataType.INTEGER,
                primary_key=True,
                nullable=False,
                unique=False,
                default=None,
                enum_values=None,
                enum_name=None,
            ),
            ColumnSchema(
                name="username",
                data_type=DataType.STRING,
                unique=True,
                nullable=False,
                primary_key=False,
                default=None,
                enum_values=None,
                enum_name=None,
            ),
            ColumnSchema(
                name="is_active",
                data_type=DataType.BOOLEAN,
                default="true",
                primary_key=False,
                nullable=True,
                unique=False,
                enum_values=None,
                enum_name=None,
            ),
        ],
    )

    generator = SchemaGenerator()
    ddl = generator.generate_ddl([table])

    print(ddl)  # For debugging output if needed

    assert "CREATE TABLE users" in ddl
    # SQLAlchemy output might vary slightly on quoting, so we check for the core parts
    assert "id INTEGER NOT NULL" in ddl
    assert "PRIMARY KEY (id)" in ddl
    assert "username VARCHAR(255) NOT NULL" in ddl
    assert "is_active BOOL" in ddl


def test_generate_enum_column_ddl():
    table = TableSchema(
        name="tasks",
        description="A table for tasks",
        columns=[
            ColumnSchema(
                name="id",
                data_type=DataType.INTEGER,
                primary_key=True,
                nullable=False,
                unique=True,
                default=None,
                enum_values=None,
                enum_name=None,
            ),
            ColumnSchema(
                name="status",
                data_type=DataType.ENUM,
                enum_values=["todo", "in_progress", "done"],
                enum_name="task_status",
                nullable=False,
                primary_key=False,
                unique=False,
                default=None,
            ),
        ],
    )

    generator = SchemaGenerator()
    ddl = generator.generate_ddl([table])

    assert "CREATE TABLE tasks" in ddl
    # Check for ENUM definition in the DDL
    # Note: SQLAlchemy dialect for MySQL typically outputs ENUM(...)
    assert "status ENUM('todo','in_progress','done') NOT NULL" in ddl


def test_generate_enum_column_missing_values():
    table = TableSchema(
        name="tasks_bad",
        description="Bad table",
        columns=[
            ColumnSchema(
                name="status",
                data_type=DataType.ENUM,
                # Missing enum_values (will be None by default)
                enum_values=None,
                enum_name=None,
                nullable=False,
                primary_key=False,
                unique=False,
                default=None,
            )
        ],
    )

    generator = SchemaGenerator()
    with pytest.raises(ValueError) as exc:
        generator.generate_ddl([table])
    assert "no enum_values defined" in str(exc.value)
