from __future__ import annotations
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class meshProject(BaseModel):
    dbtCoreProject: str
    dbtCloudProject: str
    projectId: int
    defaultEnvironmentId: int
    isProducer: bool
    isConsumer: bool
    dependentProjects: List[meshProject] = []

class publicModelNode(BaseModel):
    accountId: int
    database: str
    dbtCoreProject: str
    environmentId: int
    identifier: str
    isDefaultEnv: bool
    latestVersion: Optional[str]
    name: str
    packageName: str
    projectId: int
    publicAncestors: List[publicModelNode]
    relationName: str
    runGeneratedAt: str
    schema_: str = Field("", alias="schema")
    uniqueId: str
    
class dbtAccountMesh(BaseModel):
    meshProjects: List[meshProject]
    publicModels: List[publicModelNode]

class DiscoResponse(BaseModel):
    account: dbtAccountMesh