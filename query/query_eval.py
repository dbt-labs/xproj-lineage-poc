import requests
from schemas.eval_model_and_source import EvalDiscoResponse
import streamlit as st
import logging
import copy

from .fixtures import QUERY_ALL_MODELS, QUERY_ALL_SOURCES, QUERY_SINGLE_MODEL, QUERY_SINGLE_SOURCE

@st.cache_data
def query_metadata_cursor(input: str, api_token: str, metadata_url: str, env_id: int, after_cursor = None):

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {api_token}',
    }

    json_data = {
        'query': input,
        'variables': {
            'environmentId': env_id,
            'first': 500,
        },
    }
    if after_cursor:
        json_data["variables"]["after"] = after_cursor

    logging.info(f"Querying API with after_cursor: {after_cursor}")
    response = requests.post(metadata_url, headers=headers, json=json_data).json()

    return response


@st.cache_data
def query_all_resources(query: str, api_token: str, metadata_url: str, env_id: int, resource_type: str):

    single_call_response = query_metadata_cursor(input=query, api_token=api_token, metadata_url=metadata_url, env_id=env_id)
    all_calls_response = copy.deepcopy(single_call_response)

    while single_call_response["data"]["environment"]["definition"][resource_type]["pageInfo"]["hasNextPage"]:
        after_cursor = single_call_response["data"]["environment"]["definition"][resource_type]["pageInfo"]["endCursor"]
        single_call_response = query_metadata_cursor(input=input, api_token=api_token, metadata_url=metadata_url, env_id=env_id, after_cursor=after_cursor)
        all_calls_response["data"]["environment"]["definition"][resource_type]["edges"] += single_call_response["data"]["environment"]["applied"][resource_type]["edges"]

    return all_calls_response

@st.cache_data
def query_single_resource(resource_type: str, unique_id: str, api_token: str = st.session_state.dbt_api_token, environment_id: int = st.session_state.dbt_env_id) -> EvalDiscoResponse:
    query_map = {
        "model": QUERY_SINGLE_MODEL,
        "source": QUERY_SINGLE_SOURCE,
    }

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {api_token}',
    }

    json_data = {
        'query': query_map[resource_type],
        'variables': {
            'environmentId': environment_id,
            "uniqueIds": [unique_id],
        },
    }
    response = requests.post(st.session_state.dbt_metadata_url, headers=headers, json=json_data).json()

    return EvalDiscoResponse.parse_obj(response["data"])


def get_all_resource_unique_ids(resp, resource_type="models"):
    return set([resource["node"]["uniqueId"] for resource in resp["data"]["environment"]["definition"][resource_type]["edges"]])

def get_all_model_unique_ids():
    models = query_all_resources(query=QUERY_ALL_MODELS, api_token=st.session_state.dbt_api_token, metadata_url=st.session_state.dbt_metadata_url, env_id=st.session_state.dbt_env_id, resource_type="models")
    return get_all_resource_unique_ids(models, resource_type="models")

def get_all_source_unique_ids():
    models = query_all_resources(query=QUERY_ALL_SOURCES, api_token=st.session_state.dbt_api_token, metadata_url=st.session_state.dbt_metadata_url, env_id=st.session_state.dbt_env_id, resource_type="sources")
    return get_all_resource_unique_ids(models, resource_type="sources")

def get_all_unique_ids():
    return get_all_model_unique_ids() | get_all_source_unique_ids()