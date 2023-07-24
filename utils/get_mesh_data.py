from schemas.mesh import DiscoResponse
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config


def get_public_models_table(data: DiscoResponse):
    table_data = [
        dict(
            {
                k: public_model.model_dump(by_alias=True).get(k)
                for k in ["name", "dbtProjectName", "database", "schema"]
            }
        )
        for public_model in data.account.publicModels
    ]
    print(table_data)
    return pd.DataFrame.from_records(table_data)

def get_xproj_dag(data: DiscoResponse):
    nodes = []
    edges = []
    # build nodes
    for project in data.account.meshProjects:
        nodes.append(Node(
                id=project.dbtCoreProject,
                label=project.dbtCoreProject
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
                height=950,
                directed=True, 
                physics=False, 
                hierarchical=True,
                direction="LR"
            )

    return agraph(
        nodes=nodes, 
        edges=edges, 
        config=config
        )