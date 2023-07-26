import os
import requests
from schemas.mesh import DiscoResponse
import streamlit as st
from utils.set_variables import set_variables


from .fixtures import query_mesh_projects_and_models

@st.cache_resource
def get_mesh_projects_and_models(
    account_id: int, api_token: str
) -> DiscoResponse:
    
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    json_data = {
        "query": query_mesh_projects_and_models,
        "variables": {"accountId": account_id},
    }

    response = requests.post(st.session_state.dbt_metadata_url, headers=headers, json=json_data).json()
    print(response)
    return DiscoResponse.parse_obj(response["data"])
