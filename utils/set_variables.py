import os
import streamlit as st

def set_variables():

    # set variables we always want to seed
    if not "dbt_metadata_url" in st.session_state:
        st.session_state['dbt_metadata_url'] = "https://metadata.cloud.getdbt.com/beta/graphql"
    if not "dbt_cloud_url" in st.session_state:
        st.session_state['dbt_cloud_url'] = "https://cloud.getdbt.com"
    
    DBT_API_TOKEN = st.sidebar.text_input("dbt API Token", st.session_state.dbt_api_token if "dbt_api_token" in st.session_state else "", type="password")
    DBT_ACCOUNT_ID = st.sidebar.text_input("dbt Account ID", st.session_state.dbt_account_id if "dbt_account_id" in st.session_state else "1")
    DBT_ENV_ID = st.sidebar.text_input("dbt Environment ID (not used for mesh page)", st.session_state.dbt_env_id if "dbt_env_id" in st.session_state else "1")
    DBT_METADATA_URL = st.sidebar.text_input("Metadata URL", st.session_state.dbt_metadata_url)
    DBT_CLOUD_URL = st.sidebar.text_input("dbt Cloud URL", st.session_state.dbt_cloud_url)

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
    if not check_session_state():
        st.warning("Please set all values shown in the sidebar on the homepage.")
        st.stop()


def check_session_state():
    return (
    st.session_state.dbt_api_token and 
    st.session_state.dbt_metadata_url and 
    st.session_state.dbt_cloud_url and 
    st.session_state.dbt_account_id and 
    st.session_state.dbt_env_id
    )