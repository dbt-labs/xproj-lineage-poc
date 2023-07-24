import streamlit as st
from query.query_mesh import get_mesh_projects_and_models
from utils.get_mesh_data import get_public_models_table, get_xproj_dag

st.title("dbt Cloud Mesh")
mesh_data = get_mesh_projects_and_models()

st.subheader("Available Public models")
st.table(get_public_models_table(mesh_data))

st.subheader("dbt Mesh DAG")
get_xproj_dag(mesh_data)