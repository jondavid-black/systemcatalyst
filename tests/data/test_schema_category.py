from src.data.schema import TableSchema, ColumnSchema, DataType, DataCategory
from src.data.generator import SchemaGenerator


def test_generate_table_with_category_comment():
    table = TableSchema(
        name="controlled_table",
        description="A sensitive table",
        category=DataCategory.CONTROLLED,
        columns=[
            ColumnSchema(
                name="id",
                data_type=DataType.INTEGER,
                primary_key=True,
            ),
        ],
    )

    generator = SchemaGenerator()
    ddl = generator.generate_ddl([table])

    assert "CREATE TABLE controlled_table" in ddl
    assert "Category: controlled" in ddl
    assert "Sensitivity: internal" in ddl


def test_generate_dynamic_table_comment():
    table = TableSchema(
        name="dynamic_table",
        # no description provided
        category=DataCategory.DYNAMIC,
        columns=[
            ColumnSchema(
                name="id",
                data_type=DataType.INTEGER,
                primary_key=True,
            ),
        ],
    )

    generator = SchemaGenerator()
    ddl = generator.generate_ddl([table])

    assert "CREATE TABLE dynamic_table" in ddl
    assert "Category: dynamic" in ddl
    assert "Sensitivity: internal" in ddl
