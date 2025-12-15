from src.data.schema import TableSchema, ColumnSchema, DataType
from src.data.generator import SchemaGenerator


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
            ),
            ColumnSchema(
                name="username",
                data_type=DataType.STRING,
                unique=True,
                nullable=False,
                primary_key=False,
                default=None,
            ),
            ColumnSchema(
                name="is_active",
                data_type=DataType.BOOLEAN,
                default="true",
                primary_key=False,
                nullable=True,
                unique=False,
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
