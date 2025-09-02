from pydantic import BaseModel
from typing import Optional, Any, List


class Column(BaseModel):
    name: str
    type: str
    nullable: bool
    isPrimaryKey: bool
    defaultValue: Optional[Any]


class ForeignKey(BaseModel):
    columnName: str
    referencedTable: str
    referencedColumn: str
    constraintName: str
    updateRule: str
    deleteRule: str


class CheckConstraint(BaseModel):
    constraintName: str
    checkClause: str


class UniqueConstraint(BaseModel):
    # If you have more fields, add them here
    # For now, leaving it empty as your sample has empty lists
    pass


class Table(BaseModel):
    name: str
    columns: List[Column]
    foreignKeys: List[ForeignKey]
    checkConstraints: List[CheckConstraint]
    uniqueConstraints: List[UniqueConstraint]
    rowCount: Optional[int] = None


class SchemaPayload(BaseModel):
    success: bool
    tables: List[Table]


class DummySchema(BaseModel):
    schema: List[dict[str, Any]]
    fk_constraints: List[dict[str, Any]]
    unique_constraints: List[dict[str, Any]]
    check_constraints: List[dict[str, Any]]
