from schemas.mesh import DiscoResponse
from schemas.model_details import ExternalModelNode, ModelDiscoResponse
from streamlit_agraph import agraph, Node, Edge, Config

def get_project_colors(mesh_data: DiscoResponse):
    color_list = ["#FF694A", "#09999E", "#DE5D43", "#047377", "#F9A26C", "#D9F6F4"]
    project_list = [project.dbtCoreProject for project in mesh_data.account.meshProjects]
    color_assignment = {}
    for i, item in enumerate(project_list):
        color_assignment[item] = color_list[i % len(color_list)]
    return color_assignment

def get_model_xproj_dag(model_data: ModelDiscoResponse, mesh_data: DiscoResponse):
    colors = get_project_colors(mesh_data)
    nodes = []
    edges = []
    
    main_model = model_data.environment.definition.models.edges[0].node
    # add model
    nodes.append(Node(
            id=main_model.uniqueId,
            label=main_model.packageName + "." + main_model.name,
            shape="hexagon",
            color=colors[main_model.packageName]
        )
    )

    # add model parents
    for parent in main_model.parents:
        if not isinstance(parent, ExternalModelNode):
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
                target=main_model.uniqueId,
                source=parent.uniqueId
            )
        )

    # add model children
    for child in main_model.children:
        if not isinstance(child, ExternalModelNode):
            continue
        nodes.append(
            Node(
                id=child.uniqueId,
                label=child.dbtProjectName + "." + child.name,
                shape="hexagon",
                color=child.dbtProjectName
            )
        )
        edges.append(Edge(
                source=main_model.uniqueId,
                target=child.uniqueId
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