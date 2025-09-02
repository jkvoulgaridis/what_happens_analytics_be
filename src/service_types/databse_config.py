from typing import Any, Literal

from pydantic import BaseModel


class DBCreds(BaseModel):
    user: str
    db_name: str
    port: int
    password: str
    host: str


class DBResults(BaseModel):
    data: list[dict[str, Any]]
    sql_query: str
    plot_suggestion: Literal["pie", "bar", "line"]
    x_axis: str
    y_axis: str
    explanation: str
