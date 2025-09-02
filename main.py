import json

import streamlit as st

from src.service_types.databse_config import DBCreds
from src.sql_agent import man, run_agent_sync
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("### Database Connection & Question")

try:
    with open('./connections.json' , 'r') as file:
        connections = json.load(file)
        connections = {
            conn.get('name'): DBCreds(
                user = conn.get('user'),
                db_name = conn.get('db_name'),
                port = int(conn.get('port')),
                password = conn.get('password'),
                host = conn.get('host'),
            ) for conn in connections
        }
        connections['undefined'] = None
except Exception as e:
    print(e)
    connections = {}

col1, col2 = st.columns([1, 5])

with col1:
    st.header("Stored DB Connection")
    if connections:
        selected_connection = st.selectbox(
            "Choose a connection",
            options=list(connections.keys()),
            format_func=lambda x: x
        )
        connection = connections[selected_connection]
    st.header("DB Connection")
    user = st.text_input("User")
    db_name = st.text_input("DB Name")
    port = st.text_input("Port")
    password = st.text_input("Password", type="password")
    host = st.text_input("Host")
    if connection:
        user = user or connection.user
        db_name = db_name or connection.db_name
        port = port or connection.port
        password = password or connection.password
        host = host or connection.host

with col2:
    st.header("Ask a Question")
    question = st.text_area(
        "Your Question",
        height=150,
        placeholder="Type your question here..."
    )
    # Add a submit button
    if st.button("Submit Question", use_container_width=True):
        if question.strip():
            st.success(f"Question submitted: {question}")
            creds = DBCreds(
                user=user,
                db_name=db_name,
                port=int(port),
                password=password,
                host=host
            )
            man.update_creds(creds)
            res = run_agent_sync(question)
            plot_type = res.plot_suggestion
            x_axis = res.x_axis
            y_axis = res.y_axis
            df = pd.DataFrame(res.data)
            st.dataframe(df, use_container_width=True)  # For interactive table
        else:
            st.warning("Please enter a question before submitting.")
