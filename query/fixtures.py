query_mesh_projects_and_models = """
query Mesh($accountId: BigInt!){
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
      children {
        dbtCoreProject
        projectId
        defaultEnvironmentId
        dependentModelsCount
      }
      publicAncestors {
        uniqueId
        name
        dbtCoreProject
      }
    }
  }
}
"""

QUERY_ALL_MODELS = """
query all_models($environmentId: BigInt!, $first: Int!, $after: String) {
  environment(id: $environmentId) {
    definition {
      models(first: $first, after: $after) {
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

QUERY_SINGLE_MODEL = """
query single_model($environmentId: BigInt!, $uniqueIds: [String!]) {
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
query Environment($environmentId: BigInt!, $first: Int!, $after: String) {
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
            sourceName
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
query single_source($environmentId: BigInt!, $uniqueIds: [String!]) {
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
            sourceName
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