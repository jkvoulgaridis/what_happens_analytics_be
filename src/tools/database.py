from typing import Any, Type, Optional

from sqlalchemy import create_engine, text

from src.service_types.databse_config import DBCreds
from src.exceptions import ServiceException
from src.queries import schema_query, foreign_key_query, unique_constraint_query, check_constraint_query

from src.service_types.schema import DummySchema


class DBManager:

    def __apply_creds(self, creds: DBCreds):
        self.url = f"postgresql+psycopg2://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.db_name}"
        print(self.url)
        self.engine = create_engine(self.url)

    def __init__(
        self,
        creds: Optional[DBCreds] = None
    ) -> None:
        if not creds:
            return
        self.__apply_creds(creds)


    def update_creds(self, creds: DBCreds):
        self.__apply_creds(creds)

    def __execute_on_db(self, query: str) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            rows = [dict(row._mapping) for row in result]
            # print(rows)
        return rows

    def fetch_data(self, query: str) -> list[dict[str, Any]]:
        return self.__execute_on_db(query)

    def get_schema(self) -> Any:
        try:
            main_schema = self.__execute_on_db(schema_query)
            fks = self.__execute_on_db(foreign_key_query)
            checks = self.__execute_on_db(check_constraint_query)
            constraints = self.__execute_on_db(unique_constraint_query)
            return DummySchema(
                schema= main_schema,
                fk_constraints= fks,
                unique_constraints= constraints,
                check_constraints = checks
            )
        except Exception as e:
            raise ServiceException from e

    def execute_query(self, q: str) -> Optional[list[dict[str,Any]]]:
        return self.__execute_on_db(q)

if __name__ == '__main__':
    # data = {
    #     "user": "postgres.dnfldizzqrnabakigkue",
    #     "db_name": "postgres",
    #     "port": 5432,
    #     "password": "trading-app-db-123",
    #     "host": "aws-0-eu-central-1.pooler.supabase.com"
    # }
    data = {
        "user" : "admin",
        "db_name" : "postgres",
        "port" : "5432",
        "password" : "admin",
        "host" : "localhost",
    }
    man = DBManager(**data)
    schema = man.get_schema()
    # print(schema)
    orders = man.fetch_data("SELECT sub.asset, COUNT(io.id) AS order_count\nFROM investment_order io\nJOIN subscription sub ON io.subscription_id = sub.id\nGROUP BY sub.asset;")
    print()
    print(orders)
