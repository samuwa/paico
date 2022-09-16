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

rows = run_query("SELECT * FROM CLIENTES;")

for row in rows:
    st.write(pd.Dataframe(row))
    
#st.write(rows)
    
st.title("Ventas PAICO :earth_americas:")

col1, col2 = st.columns(2)

col2.subheader("Clientes")
col2.table(df_clientes.head())

col1.subheader("Productos")
col1.table(df_productos)

st.subheader("Ventas")
st.table(df_ventas.head(5))

st.subheader("Análisis de ventas")

col3, col4 = st.columns(2)
prods = col3.multiselect("Seleccionar Productos", df_productos["producto"])
indus = col4.multiselect("Seleccionar Industrias", df_clientes["industria"])
inicio = col3.date_input("Fecha de inicio")
cierre = col4.date_input("Fecha de cierre")

