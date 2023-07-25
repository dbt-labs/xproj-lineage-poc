import streamlit as st
from query.query_mesh import get_mesh_projects_and_models
from utils.get_mesh_data import get_public_models_table, get_xproj_dag

st.title("dbt Cloud Mesh")
mesh_data = get_mesh_projects_and_models()

st.subheader("dbt Mesh DAG")
selected_project = get_xproj_dag(mesh_data)

st.subheader(f"Available Public Models in `{selected_project}`")
st.write("Click on a project above to see the list of public models in that project.")
st.dataframe(get_public_models_table(mesh_data, selected_project))

