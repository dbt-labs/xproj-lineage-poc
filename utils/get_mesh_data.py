from schemas.mesh import DiscoResponse
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config


def get_public_models_table(data: DiscoResponse, project_name: str = None):
    table_data = [
        dict(
            {
                k: public_model.model_dump(by_alias=True).get(k)
                for k in ["name", "dbtCoreProject", "database", "schema"]
            }
        )
        for public_model in data.account.publicModels
    ]
    table_data = pd.DataFrame.from_records(table_data)
    table_data = table_data[table_data["dbtCoreProject"] == project_name]
    table_data.columns = ["Model Name", "Project Name", "Database", "Schema"]
    return table_data

def get_xproj_dag(data: DiscoResponse):
    nodes = []
    edges = []
    # build nodes
    for project in data.account.meshProjects:
        nodes.append(Node(
                id=project.dbtCoreProject,
                label=project.dbtCoreProject,
                shape="image",
                image="https://raw.githubusercontent.com/dbt-labs/docs.getdbt.com/current/website/static/img/icons/white/dbt-bit.svg",
            )
        )
    # build edges
    for project in data.account.meshProjects:
        for dependent_project in project.dependentProjects:
            edges.append(Edge(
                    target=dependent_project.dbtCoreProject,
                    source=project.dbtCoreProject
                )
            )

    # build config
    config = Config(width=750,
                height=300,
                directed=True, 
                physics=False, 
                hierarchical=True,
                nodeHighlightBehavior=True,
                highlightColor="#F7A7A6",
                collapsible=True,
                direction="LR",
            )

    return agraph(
        nodes=nodes, 
        edges=edges, 
        config=config
        )