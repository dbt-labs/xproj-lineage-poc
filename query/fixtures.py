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

query_model_details = """
query public_model_details($environmentId: Int!, $uniqueIds: [String!]){
  environment(id: $environmentId) {
    dbtProjectName
    definition {
      models(first: 1 filter: { uniqueIds: $uniqueIds }) {
        edges {
          node {
            uniqueId
            access
            name
            packageName
            parents {
              ... on ExternalModelNode {
                uniqueId
                name
                dbtProjectName
                environmentId
              }
            }
            children {
              ... on ExternalModelNode {
                uniqueId
                name
                dbtProjectName
                environmentId
              }
            }
          }
        }
      }
    }
  }
}
"""