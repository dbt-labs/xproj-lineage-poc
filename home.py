import webbrowser
import streamlit as st
from utils.fixtures import URLS
from query.query_mesh import get_mesh_projects_and_models
from utils.get_mesh_data import get_public_models_table, get_xproj_dag
from utils.set_variables import set_variables

set_variables()

st.title("dbt Mesh Workspace")
mesh_data = get_mesh_projects_and_models(st.session_state.dbt_account_id, st.session_state.dbt_api_token)

st.subheader("dbt Mesh - Project DAG")
selected_project_name = get_xproj_dag(mesh_data)
if selected_project_name:
    selected_project = [project for project in mesh_data.account.meshProjects if project.dbtCoreProject == selected_project_name][0]
    print(selected_project)

st.write("Click on a project above to see the list of public models in that project.")

if selected_project_name:
    st.subheader(f"Project Details: `{selected_project_name}`")
    if st.button("Open this project in dbt Explorer"):
        webbrowser.open_new_tab(URLS["explore"].format(**{
            'dbt_cloud_url': st.session_state.dbt_cloud_url,
            'account_id': st.session_state.dbt_account_id,
            'project_id': selected_project.projectId
        }))
    if st.button("Open this project in dbt Cloud IDE"):
        webbrowser.open_new_tab(URLS["develop"].format(**{
            'dbt_cloud_url': st.session_state.dbt_cloud_url,
            'account_id': st.session_state.dbt_account_id,
            'project_id': selected_project.projectId
        }))
    st.subheader(f"Available Public Models in `{selected_project_name}`")
    st.dataframe(get_public_models_table(mesh_data, selected_project_name), use_container_width=True)

