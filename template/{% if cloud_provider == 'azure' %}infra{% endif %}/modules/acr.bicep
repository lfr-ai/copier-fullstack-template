// ── Azure Container Registry ──────────────────────────────────────
//
// Deploys an ACR instance for container image storage with security
// hardening, managed identity, and optional geo-replication.

@description('Prefix used for resource names (e.g., myapp-dev)')
param namePrefix string

@description('Location for the ACR. Default: resource group location')
param location string = resourceGroup().location

@description('Optional registry name override')
param registryName string = ''

@description('SKU for the container registry')
@allowed(['Basic', 'Standard', 'Premium'])
param skuName string = 'Basic'

@description('Enable admin user (not recommended for production)')
param adminUserEnabled bool = false

@description('Public network access')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

@description('Data endpoint enabled (for regional endpoints)')
param dataEndpointEnabled bool = false

@description('Enable zone redundancy (Premium SKU only)')
param zoneRedundancy bool = false

@description('Geo-replication locations (Premium SKU only)')
param replicationLocations array = []

@description('Network rule bypass for Azure services')
@allowed(['AzureServices', 'None'])
param networkRuleBypassOptions string = 'AzureServices'

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

// ── Derived values ───────────────────────────────────────────────

// ACR names must be globally unique, 5-50 chars, alphanumeric only
var sanitizedPrefix = replace(replace(namePrefix, '-', ''), '_', '')
var acrName = empty(registryName) ? '${sanitizedPrefix}acr' : registryName

// ── Container Registry ───────────────────────────────────────────

resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = if (enabled) {
  name: acrName
  location: location
  sku: {
    name: skuName
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    adminUserEnabled: adminUserEnabled
    publicNetworkAccess: publicNetworkAccess
    dataEndpointEnabled: dataEndpointEnabled
    zoneRedundancy: (skuName == 'Premium' && zoneRedundancy) ? 'Enabled' : 'Disabled'
    networkRuleBypassOptions: networkRuleBypassOptions
    policies: {
      retentionPolicy: {
        days: skuName == 'Premium' ? 30 : 7
        status: 'enabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: skuName == 'Premium' ? 'enabled' : 'disabled'
      }
    }
  }
  tags: tags
}

// ── Geo-replication (Premium only) ───────────────────────────────

resource replications 'Microsoft.ContainerRegistry/registries/replications@2023-11-01-preview' = [
  for repl in replicationLocations: if (enabled && skuName == 'Premium' && !empty(replicationLocations)) {
    parent: acr
    name: repl
    location: repl
    properties: {
      zoneRedundancy: zoneRedundancy ? 'Enabled' : 'Disabled'
    }
  }
]

// ── Outputs ──────────────────────────────────────────────────────

output registryName string = enabled ? acr.name : ''
output registryLoginServer string = enabled ? acr.properties.loginServer : ''
output registryResourceId string = enabled ? acr.id : ''
output registryPrincipalId string = enabled ? acr.identity.principalId : ''
