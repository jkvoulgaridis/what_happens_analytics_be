import asyncio
from typing import Any, Optional

from agents import Agent, Runner, function_tool, RunContextWrapper, trace, AgentOutputSchema

from src.service_types.databse_config import DBResults
from src.service_types.schema import DummySchema
from src.tools.database import DBManager


man = DBManager()


@function_tool(name_override="get_schema")
async def get_schema(ctx: RunContextWrapper[Any]) -> DummySchema:
    return man.get_schema()


@function_tool(name_override="get_results")
async def get_results(ctx: RunContextWrapper[Any], query: str) -> list[dict[str, Any]]:
    return man.fetch_data(query)


sql_agent = Agent(
    name="SQL agent",
    instructions="""
    You are an agent expert in SQL. You translate queries 
    from natural language into SQL queries which you can also run.
    Given the Natural Language Query, you can use the get_schema to 
    fetch the schema of the database, which include the tables, along with 
    the columns, Foreign Key relationships and constraints. Based, on that,
    generate a postgres SQL query and then you must use the get_results 
    with the generated query to get the results, which should be printed in the screen.
    Once we have the results, we should also propose a visualisation method (include the x-axis and y-axis of the chart) 
    from the available options 
    for those data along with a brief explanation on the results and the chain of thought you followed based
    on available data and tables and the sql query you used. If for any case you cannot connect to the db 
    or retrieve results you should returns an empty response.
    """,
    model="gpt-4o",
    tools=[get_schema, get_results],
    output_type=AgentOutputSchema(Optional[DBResults], strict_json_schema=False)
)


async def run_agent(input_query: str) -> DBResults:
    from dotenv import load_dotenv
    load_dotenv(override=True)
    with trace("SQL Insights agent"):
        res = await Runner.run(sql_agent, input_query)
    return res.final_output


def run_agent_sync(input_query: str) -> DBResults:
    return asyncio.run(run_agent(input_query))


