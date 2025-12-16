from src.data.schema import (
    TableSchema,
    ColumnSchema,
    DataType,
    DataCategory,
    DataSensitivity,
    RetentionPolicy,
)
from src.data.generator import SchemaGenerator


def test_generate_table_with_all_metadata():
    table = TableSchema(
        name="sensitive_table",
        description="A table with sensitive data",
        category=DataCategory.CONTROLLED,
        namespace="security",
        owner="Security Team",
        sensitivity=DataSensitivity.PII,
        retention=RetentionPolicy.FISCAL_YEAR,
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

    assert "CREATE TABLE sensitive_table" in ddl
    # Check that all metadata is included in the comment
    expected_comment = (
        "A table with sensitive data (Category: controlled, Namespace: security, "
        "Owner: Security Team, Sensitivity: pii, Retention: fiscal_year)"
    )
    assert f"COMMENT='{expected_comment}'" in ddl


def test_generate_table_with_composite_unique_constraint():
    table = TableSchema(
        name="constrained_table",
        description="Table with unique constraints",
        columns=[
            ColumnSchema(
                name="id",
                data_type=DataType.INTEGER,
                primary_key=True,
            ),
            ColumnSchema(
                name="col_a",
                data_type=DataType.STRING,
            ),
            ColumnSchema(
                name="col_b",
                data_type=DataType.STRING,
            ),
        ],
        composite_unique_constraints=[["col_a", "col_b"]],
    )

    generator = SchemaGenerator()
    ddl = generator.generate_ddl([table])

    assert "CREATE TABLE constrained_table" in ddl
    assert "UNIQUE (col_a, col_b)" in ddl


def test_generate_table_default_metadata():
    table = TableSchema(
        name="default_table",
        # No description or extra metadata provided
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

    # Should fall back to defaults
    # controlled, internal, indefinite
    expected_comment = (
        "(Category: controlled, Sensitivity: internal, Retention: indefinite)"
    )
    assert f"COMMENT='{expected_comment}'" in ddl
