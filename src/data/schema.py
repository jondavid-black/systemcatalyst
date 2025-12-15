from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class DataType(str, Enum):
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    TIMESTAMP = "timestamp"
    JSON = "json"
    ENUM = "enum"


class EnumSchema(BaseModel):
    name: str = Field(description="The name of the enum")
    values: List[str] = Field(description="The allowed values for the enum")
    description: Optional[str] = Field(
        default=None, description="Description of the enum"
    )


class ColumnSchema(BaseModel):
    name: str = Field(description="The name of the column")
    data_type: DataType = Field(description="The data type of the column")
    primary_key: bool = Field(
        default=False, description="Whether this column is a primary key"
    )
    nullable: bool = Field(default=True, description="Whether this column can be null")
    unique: bool = Field(
        default=False, description="Whether this column must be unique"
    )
    default: Optional[str] = Field(
        default=None, description="Default value for the column (as a string)"
    )
    enum_values: Optional[List[str]] = Field(
        default=None, description="List of allowed values for ENUM type"
    )
    enum_name: Optional[str] = Field(
        default=None, description="Name of the ENUM type (if applicable)"
    )


class TableSchema(BaseModel):
    name: str = Field(description="The name of the table")
    columns: List[ColumnSchema] = Field(description="List of columns in the table")
    description: Optional[str] = Field(
        default=None, description="Description of the table"
    )
