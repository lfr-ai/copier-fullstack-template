// ── Azure OpenAI Service ───────────────────────────────────────────
// Deploys an Azure OpenAI account (Microsoft.CognitiveServices/accounts
// kind: OpenAI) with configurable model deployments for chat completion
// and embeddings, suitable for RAG pipelines.

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the Azure OpenAI account. Default: resource group location')
param location string = resourceGroup().location

@description('Optional account name')
param accountName string = ''

@description('SKU name for the Cognitive Services account')
param skuName string = 'S0'

@description('Custom sub-domain name for token-based auth')
param customSubDomainName string = ''

@description('Public network access')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

@description('Disable local (API key) authentication in favour of Entra ID')
param disableLocalAuth bool = false

@description('Chat completion model deployment name')
param chatModelName string = 'gpt-4o'

@description('Chat model version')
param chatModelVersion string = '2024-08-06'

@description('Chat model deployment SKU name')
param chatDeploymentSkuName string = 'Standard'

@description('Chat model deployment capacity (thousands of tokens per minute)')
param chatDeploymentCapacity int = 10

@description('Embedding model deployment name')
param embeddingModelName string = 'text-embedding-3-large'

@description('Embedding model version')
param embeddingModelVersion string = ''

@description('Embedding model deployment SKU name')
param embeddingDeploymentSkuName string = 'Standard'

@description('Embedding model deployment capacity (thousands of tokens per minute)')
param embeddingDeploymentCapacity int = 10

@description('Deploy the chat model')
param deployChatModel bool = true

@description('Deploy the embedding model')
param deployEmbeddingModel bool = true

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var oaiName = empty(accountName) ? '${namePrefix}-oai' : accountName
var subdomain = empty(customSubDomainName) ? oaiName : customSubDomainName

resource openai 'Microsoft.CognitiveServices/accounts@2024-10-01' = if (enabled) {
  name: oaiName
  location: location
  kind: 'OpenAI'
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: skuName
  }
  properties: {
    customSubDomainName: subdomain
    publicNetworkAccess: publicNetworkAccess
    disableLocalAuth: disableLocalAuth
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: publicNetworkAccess == 'Disabled' ? 'Deny' : 'Allow'
      ipRules: []
      virtualNetworkRules: []
    }
  }
  tags: tags
}

// ── Chat Completion Model ────────────────────────────────────────

resource chatDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = if (enabled && deployChatModel) {
  parent: openai
  name: chatModelName
  sku: {
    name: chatDeploymentSkuName
    capacity: chatDeploymentCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: chatModelName
      version: chatModelVersion
    }
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}

// ── Embedding Model ──────────────────────────────────────────────

resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = if (enabled && deployEmbeddingModel) {
  parent: openai
  name: embeddingModelName
  sku: {
    name: embeddingDeploymentSkuName
    capacity: embeddingDeploymentCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      version: embeddingModelVersion
    }
  }
  dependsOn: [
    chatDeployment
  ]
}

output openaiAccountName string = enabled ? openai.name : ''
output openaiAccountId string = enabled ? openai.id : ''
output openaiEndpoint string = enabled ? openai.properties.endpoint : ''
output openaiPrincipalId string = enabled ? openai.identity.principalId : ''
