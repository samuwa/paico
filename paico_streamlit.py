import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("selext * from clientes")

for row in rows:
    st.write(row)
