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

clientes_query = run_query("SELECT * FROM CLIENTES;")

clientes = pd.DataFrame({x for x in clientes_query}, columns=["clienteid","cliente","pais","industria"])

ventas_query = run_query("SELECT * FROM VENTAS;")

ventas = pd.DataFrame({x for x in ventas_query}, columns=["clienteid", "productoid", "total", "fecha"])

st.write(clientes)
st.write(ventas)

# for row in rows:
#     st.write(row)
    
# st.table(pd.DataFrame(rows, columns=cur.description))
    
st.title("Ventas PAICO :earth_americas:")

col1, col2 = st.columns(2)

col2.subheader("Clientes")


col1.subheader("Productos")


st.subheader("Ventas")


st.subheader("Análisis de ventas")

col3, col4 = st.columns(2)
prods = col3.multiselect("Seleccionar Productos", df_productos["producto"])
indus = col4.multiselect("Seleccionar Industrias", df_clientes["industria"])
inicio = col3.date_input("Fecha de inicio")
cierre = col4.date_input("Fecha de cierre")

