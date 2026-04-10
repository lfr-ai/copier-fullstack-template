// ── Azure Document Intelligence (Form Recognizer) ──────────────────
// Deploys an Azure AI Document Intelligence account for extracting
// text, tables, and structure from PDFs and documents — a critical
// component of the RAG ingestion pipeline.

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the account. Default: resource group location')
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

@description('Disable local (API key) authentication in favor of Entra ID')
param disableLocalAuth bool = false

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var diName = empty(accountName) ? '${namePrefix}-docintl' : accountName
var subdomain = empty(customSubDomainName) ? diName : customSubDomainName

resource docIntelligence 'Microsoft.CognitiveServices/accounts@2024-10-01' = if (enabled) {
  name: diName
  location: location
  kind: 'FormRecognizer'
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

output docIntelligenceName string = enabled ? docIntelligence.name : ''
output docIntelligenceId string = enabled ? docIntelligence.id : ''
output docIntelligenceEndpoint string = enabled ? docIntelligence.properties.endpoint : ''
output docIntelligencePrincipalId string = enabled ? docIntelligence.identity.principalId : ''
