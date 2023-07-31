
import streamlit as st
from utils.set_variables import check_session_state, set_variables, check_variables


st.set_page_config(
    page_title="dbt mesh Explorer",
    page_icon="👋",
    
)

st.write("# Welcome to the dbt mesh Explorer and Project Evaluator beta! 👋")
st.write("Click on the pages to the left to explore the mesh and get recommendations for your dbt projects.")
st.header("dbt mesh Explorer")
st.write("This page allows you to explore the dbt mesh and see the lineage of public models in your dbt Account.")
st.header("`dbt_project_evaluator`")
st.write("This page allows you to see best practice recommendations for the models and sources in your dbt projects.")
st.markdown("This represents a subset of the rules found in the [dbt package](https://hub.getdbt.com/dbt-labs/dbt_project_evaluator/latest/) of the same name!")


set_variables()
check_variables()