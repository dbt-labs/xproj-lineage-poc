import requests
from schemas.mesh import DiscoResponse
from schemas.public_model_details import ModelDiscoResponse
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
    if response.get("errors"):
        st.warning("Error querying the Discovery API: " + [error.get("message") for error in response.get("errors")][0])
        st.stop()
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
    if response.get("errors"):
        st.warning("Error querying the Discovery API: " + [error.get("message") for error in response.get("errors")][0])
        st.stop()
    return ModelDiscoResponse.parse_obj(response["data"])