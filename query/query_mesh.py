import requests
from schemas.mesh import DiscoResponse
from schemas.model_details import ModelDiscoResponse
import streamlit as st

from .fixtures import query_mesh_projects_and_models, query_model_details

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
    return DiscoResponse.parse_obj(response["data"])


def get_public_model_details(unique_id: str, environment_id: int, api_token: str) -> ModelDiscoResponse:
    
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    json_data = {
        "query": query_model_details,
        "variables": {"environmentId": environment_id, "uniqueIds": [unique_id]},
    }

    response = requests.post(st.session_state.dbt_metadata_url, headers=headers, json=json_data).json()
    print(environment_id)
    return ModelDiscoResponse.parse_obj(response["data"])