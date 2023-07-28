from __future__ import annotations
from typing import Dict, List, Union
from pydantic import BaseModel

class ExternalModelNode(BaseModel):
    uniqueId: str
    name: str
    dbtProjectName: str
    environmentId: int

class SimplePublicModel(BaseModel):
    uniqueId: str
    access: str
    name: str
    packageName: str
    parents: List[Union[ExternalModelNode, Dict[str, str]]] = []
    children: List[Union[ExternalModelNode, Dict[str, str]]] = []

class SimpleNode(BaseModel):
    node: SimplePublicModel

class PublicModelEdges(BaseModel):
    edges: List[SimpleNode]

class DiscoveryModelDefinitionState(BaseModel):
    models: PublicModelEdges

class dbtEnviromentResponse(BaseModel):
    dbtProjectName: str
    definition: DiscoveryModelDefinitionState

class ModelDiscoResponse(BaseModel):
    environment: dbtEnviromentResponse