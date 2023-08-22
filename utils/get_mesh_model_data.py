from schemas.mesh import DiscoResponse, publicAncestor, publicModelNode
from schemas.public_model_details import ExternalModelNode, ModelDiscoResponse
from streamlit_agraph import agraph, Node, Edge, Config

def get_project_colors(mesh_data: DiscoResponse):
    color_list = ["#FF694A", "#09999E", "#DE5D43", "#047377", "#F9A26C", "#D9F6F4"]
    project_list = [project.dbtCoreProject for project in mesh_data.account.meshProjects]
    color_assignment = {}
    for i, item in enumerate(project_list):
        color_assignment[item] = color_list[i % len(color_list)]
    return color_assignment

def get_model_xproj_dag(model_data: publicModelNode, mesh_data: DiscoResponse):
    colors = get_project_colors(mesh_data)
    nodes = []
    edges = []
    
    # add model
    nodes.append(Node(
            id=model_data.uniqueId,
            label=model_data.packageName + "." + model_data.name,
            shape="hexagon",
            color=colors[model_data.packageName]
        )
    )

    # add model parents
    for parent in model_data.publicAncestors:
        if not isinstance(parent, publicAncestor):
            continue
        nodes.append(
            Node(
                id=parent.uniqueId,
                label=parent.dbtProjectName + "." + parent.name,
                shape="hexagon",
                color=parent.dbtProjectName
            )
        )
        edges.append(Edge(
                target=model_data.uniqueId,
                source=parent.uniqueId
            )
        )

    # add model project-level children
    for child in model_data.children:
        if child.dependentModelsCount == 0:
            continue
        nodes.append(
            Node(
                id=child.dbtCoreProject,
                label=f"Used by {child.dependentModelsCount} model(s) in project {child.dbtCoreProject}",
                shape="square",
                color=colors[child.dbtCoreProject]
            )
        )
        edges.append(Edge(
                source=model_data.uniqueId,
                target=child.dbtCoreProject
            )
        )

    # build config
    config = Config(width=750,
                height=300,
                nodeSpacing=400,
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