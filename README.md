## What Happens Analytics

This is a project building an end-to-end
functionality for low code/ no code users to access 
databases directly and query in natural language.

The project implements: 

* A tool for connecting to the DB and get the schema, FK 
    relationships and DB constraints.
* A tool to execute arbitrary queries on the connected DB. 
* An agent that uses both tools, translates natural language
    queries to Postgres SQL and executes it, returning results. 
* A streamlit UI giving functionality to add DB credentials, connect to DB 
    and query as well as a tabular view of the results. 

## Running the lizard

0. OPENAI KEY setup: Create a `.env` file and add the `OPENAI_API_KEY`. 


1. Env setup

```commandline
python -v venv .venv
pip install uv
uv sync
```

2. (Optional) Show src to project 
```commandline
PYTHONPATH=$(pwd)
```

2. Launch streamlit UI

```commandline
 streamlit run main.py
```

4. Navigate to `http://localhost:8501/`  and play around. 

5. (Optional) If you have mutliple DBS (for example a local one, a DB hoston AWS and a supabase)
    you can configure a file named `connections.json` with the format: 

```commandline
  [
  {  "name": "Local DB",
    "user": "admin",
    "db_name": "pgdb",
    "port": 5423,
    "password": "admin",
    "host": "localhost"
  }, 
  
  ]
```

and those connection will appear as a dropdown list for avoiding inputing 
credentials all the time. 


## Disclaimer

1. This is a toy project with very limited functionality and very low security. 