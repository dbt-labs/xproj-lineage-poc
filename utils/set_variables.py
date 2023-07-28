import os
import streamlit as st

def set_variables():
    # todo - allow user to set these in app
    DBT_API_TOKEN = st.sidebar.text_input("dbt API Token", type="password")
    DBT_ACCOUNT_ID = st.sidebar.text_input("dbt Account ID", "1")
    DBT_ENV_ID = st.sidebar.text_input("dbt Environment ID (not used for mesh page)", "1")
    DBT_METADATA_URL = st.sidebar.text_input("Metadata URL", "https://metadata.cloud.getdbt.com/beta/graphql")
    DBT_CLOUD_URL = st.sidebar.text_input("dbt Cloud URL", "https://cloud.getdbt.com")

    # store variables in session state
    for variable in [
        {"key": "dbt_api_token", "value": DBT_API_TOKEN},
        {"key": "dbt_metadata_url", "value": DBT_METADATA_URL},
        {"key": "dbt_cloud_url", "value": DBT_CLOUD_URL},
        {"key": "dbt_account_id", "value": int(DBT_ACCOUNT_ID)},
        {"key": "dbt_env_id", "value": int(DBT_ENV_ID)},
    ]:
        st.session_state[variable["key"]] = variable["value"]
    

def check_variables():
    if not (
    st.session_state.dbt_api_token and 
    st.session_state.dbt_metadata_url and 
    st.session_state.dbt_cloud_url and 
    st.session_state.dbt_account_id and 
    st.session_state.dbt_env_id
    ):
        st.warning("Please set all values shown in the sidebar on the homepage.")
        st.stop()