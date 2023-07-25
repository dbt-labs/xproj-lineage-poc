import os
import requests
from schemas.mesh import DiscoResponse
import streamlit as st


from .fixtures import query_mesh_projects_and_models

# todo - allow user to set these in app
DBT_API_TOKEN = os.getenv("DBT_API_TOKEN")
DBT_METADATA_URL = os.getenv("DBT_METADATA_URL") or "https://metadata.cloud.getdbt.com/beta/graphql"
DBT_ENV_ID = int(os.getenv("DBT_ENV_ID"))
DBT_ACCOUNT_ID = int(os.getenv("DBT_ACCOUNT_ID"))

@st.cache_resource
def get_mesh_projects_and_models(account_id: int = DBT_ACCOUNT_ID, api_token: str = DBT_API_TOKEN) -> DiscoResponse:
    
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {api_token}',
    }

    json_data = {
        'query': query_mesh_projects_and_models,
        'variables': {
            'accountId': account_id
        },
    }
    response = requests.post(DBT_METADATA_URL, headers=headers, json=json_data).json()
    return DiscoResponse.parse_obj(response['data'])