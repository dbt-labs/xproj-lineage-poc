query_mesh_projects_and_models = """
query Mesh($accountId: Int!){
  account(id: $accountId) {
    meshProjects {
      dbtCoreProject
      dbtCloudProject
      projectId
      defaultEnvironmentId
      isProducer
      isConsumer
      dependentProjects {
        dbtCoreProject
        dbtCloudProject
        projectId
        defaultEnvironmentId
        isProducer
        isConsumer
      }
    }
    publicModels {
      uniqueId
      dbtProject
      dbtProjectName
      projectId
      environmentId
      accountId
      isDefaultEnv
      name
      packageName
      latestVersion
      relationName
      database
      schema
      identifier
      runGeneratedAt
      publicAncestors {
        name
        packageName
        relationName
      }
    }
  }
}
"""