import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

# Crear conexión
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
 

# Queries para tablas
clientes_query = run_query("SELECT * FROM CLIENTES;")

clientes = pd.DataFrame({x for x in clientes_query}, columns=["clienteid","cliente","pais","industria"])

ventas_query = run_query("SELECT * FROM VENTAS;")

ventas = pd.DataFrame({x for x in ventas_query}, columns=["clienteid", "productoid", "total", "fecha"])

productos_query = run_query("SELECT * FROM PRODUCTOS;")

productos = pd.DataFrame({x for x in productos_query}, columns=["productoid", "producto", "origen"])

# for row in rows:
#     st.write(row)
    
# st.table(pd.DataFrame(rows, columns=cur.description))
    
st.title("Ventas PAICO :earth_americas:")

col1, col2 = st.columns(2)

col1.subheader("Clientes")
col1.table(clientes)


col2.subheader("Productos")
col2.table(productos)


st.subheader("Ventas")
st.table(ventas.head(10))


st.subheader("Análisis de ventas")

col3, col4 = st.columns(2)
prods = col3.multiselect("Seleccionar Productos", productos["producto"])
indus = col4.multiselect("Seleccionar Industrias", clientes["industria"])
inicio = col3.date_input("Fecha de inicio")
cierre = col4.date_input("Fecha de cierre")


total_industria_query = run_query(f"select clientes.industria, sum(ventas.total) from clientes join ventas on ventas.cliente = clientes.clienteidwhere clientes.industria in {set(indus)} group by clientes.industria")
total_industria_df = pd.DataFrame(total_industria_query, columns=["Industria", "Total"])
st.write(total_industria_df)                                  
                                
