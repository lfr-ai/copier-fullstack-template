// ── Log Analytics Workspace ───────────────────────────────────────

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the Log Analytics workspace. Default: resource group location')
param location string = resourceGroup().location

@description('Optional workspace name')
param workspaceName string = ''

@description('Retention in days for logs. Default: 90')
@allowed([30, 60, 90, 120, 180, 270, 365, 550, 730])
param retentionInDays int = 90

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var lawName = empty(workspaceName) ? '${namePrefix}-law' : workspaceName

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = if (enabled) {
  name: lawName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: retentionInDays
  }
  tags: tags
}

output logAnalyticsName string = enabled ? law.name : ''
output logAnalyticsResourceId string = enabled ? law.id : ''
output logAnalyticsCustomerId string = enabled
  ? reference(resourceId('Microsoft.OperationalInsights/workspaces', law.name), '2023-09-01').customerId
  : ''
