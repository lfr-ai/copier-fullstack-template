// ── Azure AI Search ────────────────────────────────────────────────
// Deploys an Azure AI Search service with vector search, semantic
// ranking, and hybrid search capabilities for RAG pipelines.

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the search service. Default: resource group location')
param location string = resourceGroup().location

@description('Optional search service name')
param searchServiceName string = ''

@description('SKU name for the search service')
@allowed(['free', 'basic', 'standard', 'standard2', 'standard3', 'storage_optimized_l1', 'storage_optimized_l2'])
param skuName string = 'basic'

@description('Number of replicas (1–12 for standard SKUs, 1–3 for basic)')
@minValue(1)
@maxValue(12)
param replicaCount int = 1

@description('Number of partitions (1, 2, 3, 4, 6, or 12 for standard SKUs)')
@minValue(1)
@maxValue(12)
param partitionCount int = 1

@description('Semantic search configuration')
@allowed(['disabled', 'free', 'standard'])
param semanticSearch string = 'free'

@description('Hosting mode')
@allowed(['default', 'highDensity'])
param hostingMode string = 'default'

@description('Public network access')
@allowed(['enabled', 'disabled'])
param publicNetworkAccess string = 'enabled'

@description('Disable local (API key) authentication in favour of RBAC')
param disableLocalAuth bool = false

@description('Authentication options: apiKeyOnly or aadOrApiKey')
param authOptions object = {
  aadOrApiKey: {
    aadAuthFailureMode: 'http401WithBearerChallenge'
  }
}

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var searchName = empty(searchServiceName) ? '${namePrefix}-search' : searchServiceName

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = if (enabled) {
  name: searchName
  location: location
  sku: {
    name: skuName
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    replicaCount: replicaCount
    partitionCount: partitionCount
    hostingMode: hostingMode
    semanticSearch: semanticSearch
    publicNetworkAccess: publicNetworkAccess
    disableLocalAuth: disableLocalAuth
    authOptions: disableLocalAuth ? null : authOptions
    networkRuleSet: {
      bypass: 'AzureServices'
      ipRules: []
    }
  }
  tags: tags
}

output searchServiceName string = enabled ? search.name : ''
output searchServiceId string = enabled ? search.id : ''
output searchServiceEndpoint string = enabled ? 'https://${search.name}.search.windows.net' : ''
output searchServicePrincipalId string = enabled ? search.identity.principalId : ''
