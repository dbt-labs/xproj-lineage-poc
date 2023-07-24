import streamlit as st
from query.query_mesh import get_mesh_projects_and_models

st.title("dbt Cloud Mesh")
mesh_data = get_mesh_projects_and_models()
st.write(mesh_data)