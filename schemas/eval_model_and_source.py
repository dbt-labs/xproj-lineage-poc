from __future__ import annotations
from typing import List, Union
from pydantic import BaseModel, Field

class DiscoRelatedDAGNode(BaseModel):
    name: str
    uniqueId: str

class DiscoRelatedTestNode(BaseModel):
    name: str
    uniqueId: str
    columnName: Union[str, None] = ""

class DiscoPageInfo(BaseModel):
    hasNextPage: bool
    startCursor: Union[str, None] = None
    endCursor: Union[str, None] = None

class DiscoModelNode(BaseModel):
    name: str
    uniqueId: str
    description: str
    materializedType: str
    parents: List[DiscoRelatedDAGNode]
    children: List[DiscoRelatedDAGNode]
    tests: List[DiscoRelatedTestNode]

class DiscoSourceNode(BaseModel):
    name: str
    uniqueId: str
    description: str
    database: str
    sourceName: str
    schema_: str = Field("", alias="schema")
    children: List[DiscoRelatedDAGNode]
    tests: List[DiscoRelatedTestNode]


class DiscoNode(BaseModel):
    node: Union[DiscoModelNode, DiscoSourceNode]

class DiscoModelDefinitionResponse(BaseModel):
    edges: List[DiscoNode]
    totalCount: int
    pageInfo: DiscoPageInfo

class DiscoSourceDefinitionResponse(BaseModel):
    edges: List[DiscoNode] = []
    totalCount: int
    pageInfo: DiscoPageInfo

class DiscoModelsDefinitionResponse(BaseModel):
    models: DiscoModelDefinitionResponse

class DiscoSourcesDefinitionResponse(BaseModel):
    sources: DiscoSourceDefinitionResponse

class DiscoEnvironmentResponse(BaseModel):
    definition: Union[DiscoModelsDefinitionResponse, DiscoSourcesDefinitionResponse]

class EvalDiscoResponse(BaseModel):
    environment: DiscoEnvironmentResponse