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
      dbtCoreProject
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

QUERY_ALL_MODELS = """
query all_models($environmentId: Int!, $first: Int!, $after: String) {
  environment(id: $environmentId) {
    definition {
      models(first: $first, after: $after) {
        edges {
          node {
            parents {
              uniqueId
              name
            }
            name
            uniqueId
          }
        }
        totalCount
        pageInfo {
          hasNextPage
          startCursor
          endCursor
        }
      }
    }
  }
}
"""

QUERY_SINGLE_MODEL = """
query single_model($environmentId: Int!, $uniqueIds: [String!]) {
  environment(id: $environmentId) {
    definition {
      models(first: 1, filter: { uniqueIds: $uniqueIds }) {
        edges {
          node {
            parents {
              uniqueId
              name
            }
            children {
              uniqueId
              name
            }
            tests {
              uniqueId
              name
              columnName
            }
            name
            uniqueId
            description
            materializedType
          }
        }
        totalCount
        pageInfo {
          hasNextPage
          startCursor
          endCursor
        }
      }
    }
  }
}
"""

QUERY_ALL_SOURCES = """
query Environment($environmentId: Int!, $first: Int!, $after: String) {
  environment(id: $environmentId) {
    definition {
      sources(first: $first, after: $after) {
        edges {
          node {
            children {
              uniqueId
              name
            }
            name
            uniqueId
            database
            description
            schema
            tests {
              name
              uniqueId
              columnName
            }
          }
        }
        totalCount
        pageInfo {
          hasNextPage
          startCursor
          endCursor
        }
      }
    }
  }
}
"""

QUERY_SINGLE_SOURCE = """
query single_source($environmentId: Int!, $uniqueIds: [String!]) {
  environment(id: $environmentId) {
    definition {
      sources(first: 1, filter: { uniqueIds: $uniqueIds }) {
        edges {
          node {
            children {
              uniqueId
              name
            }
            name
            uniqueId
            database
            description
            schema
            tests {
              name
              uniqueId
              columnName
            }
          }
        }
        totalCount
        pageInfo {
          hasNextPage
          startCursor
          endCursor
        }
      }
    }
  }
}
"""