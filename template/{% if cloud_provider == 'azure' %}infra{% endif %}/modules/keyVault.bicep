// ── Key Vault ─────────────────────────────────────────────────────

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the Key Vault. Default: resource group location')
param location string = resourceGroup().location

@description('SKU name for the Key Vault. Default: standard')
param skuName string = 'standard'

@description('Optional Key Vault name')
param keyVaultName string = ''

@description('Principal ids (objectIds) to grant secret permissions to.')
param principalIds array = []

@description('Tags to apply')
param tags object = {}

@description('Enable soft-delete. Once enabled it cannot be disabled. Default: true')
param enableSoftDelete bool = true

@description('Enable purge protection. Requires soft-delete enabled. Default: true')
param enablePurgeProtection bool = true

@description('Enable Azure RBAC authorization for data plane operations. Default: true')
param enableRbacAuthorization bool = true

@description('Soft-delete retention period in days. Default: 90')
@minValue(7)
@maxValue(90)
param softDeleteRetentionInDays int = 90

@description('Public network access. Default: Enabled')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

@description('Network ACLs object.')
param networkAcls object = {
  bypass: 'AzureServices'
  defaultAction: 'Deny'
  ipRules: []
  virtualNetworkRules: []
}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var kvName = empty(keyVaultName) ? '${namePrefix}-kv' : keyVaultName
var principalPolicies = [
  for id in principalIds: {
    tenantId: subscription().tenantId
    objectId: id
    permissions: {
      secrets: ['get', 'list', 'set', 'delete']
    }
  }
]

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = if (enabled) {
  name: kvName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: skuName
    }
    accessPolicies: enableRbacAuthorization ? [] : principalPolicies
    enableSoftDelete: enableSoftDelete
    enablePurgeProtection: enablePurgeProtection
    enableRbacAuthorization: enableRbacAuthorization
    softDeleteRetentionInDays: softDeleteRetentionInDays
    publicNetworkAccess: publicNetworkAccess
    networkAcls: networkAcls
  }
  tags: tags
}

output keyVaultName string = enabled ? kv.name : ''
output keyVaultUri string = enabled ? 'https://${kv.name}${environment().suffixes.keyvaultDns}/' : ''
output keyVaultResourceId string = enabled ? resourceId('Microsoft.KeyVault/vaults', kv.name) : ''
