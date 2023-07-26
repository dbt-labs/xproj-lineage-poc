import os
import streamlit as st

def set_variables():
    # todo - allow user to set these in app
    DBT_API_TOKEN = os.getenv("DBT_API_TOKEN")
    DBT_ACCOUNT_ID = os.getenv("DBT_ACCOUNT_ID")
    if not DBT_API_TOKEN:
        DBT_API_TOKEN = st.sidebar.text_input("dbt API Token", type="password")
    if not DBT_ACCOUNT_ID:
        DBT_ACCOUNT_ID = st.sidebar.text_input("dbt Account ID")
    
    DBT_METADATA_URL = st.sidebar.text_input("Metadata URL", "https://metadata.cloud.getdbt.com/beta/graphql")
    DBT_CLOUD_URL = st.sidebar.text_input("dbt Cloud URL", "https://cloud.getdbt.com")

    # store variables in session state
    for variable in [
        {"key": "dbt_api_token", "value": DBT_API_TOKEN},
        {"key": "dbt_metadata_url", "value": DBT_METADATA_URL},
        {"key": "dbt_cloud_url", "value": DBT_CLOUD_URL},
        {"key": "dbt_account_id", "value": int(DBT_ACCOUNT_ID) if DBT_ACCOUNT_ID else None},
    ]:
        st.session_state[variable["key"]] = variable["value"]
    
    if not (
    st.session_state.dbt_api_token and 
    st.session_state.dbt_metadata_url and 
    st.session_state.dbt_account_id
    ):
        st.warning("Please set all values shown in the sidebar.")
        st.stop()