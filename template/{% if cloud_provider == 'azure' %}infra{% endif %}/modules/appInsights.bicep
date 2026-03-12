// ── Application Insights ──────────────────────────────────────────

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the application insights. Default: resource group location')
param location string = resourceGroup().location

@description('Resource kind used to customize UI. Default: web')
param kind string = 'web'

@description('Application type. Default: web')
@allowed(['web', 'other'])
param applicationType string = 'web'

@description('Resource Id of the Log Analytics workspace to send data to')
param workspaceResourceId string = ''

@description('Public network access mode for ingestion endpoint. Default: Enabled')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccessForIngestion string = 'Enabled'

@description('Public network access mode for query endpoint. Default: Enabled')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccessForQuery string = 'Enabled'

@description('Data retention in days. Default: 90')
@allowed([30, 60, 90, 120, 180, 270, 365, 550, 730])
param retentionInDays int = 90

@description('Disable non-AAD based authentication. Default: true')
param disableLocalAuth bool = true

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var appiName = '${namePrefix}-appi'

resource appi 'Microsoft.Insights/components@2020-02-02' = if (enabled) {
  name: appiName
  location: location
  kind: kind
  properties: union(
    {
      Application_Type: applicationType
      publicNetworkAccessForIngestion: publicNetworkAccessForIngestion
      publicNetworkAccessForQuery: publicNetworkAccessForQuery
      RetentionInDays: retentionInDays
      DisableLocalAuth: disableLocalAuth
      Request_Source: 'rest'
    },
    empty(workspaceResourceId)
      ? {}
      : {
          WorkspaceResourceId: workspaceResourceId
        }
  )
  tags: tags
}

output appInsightsName string = enabled ? appi.name : ''
output appInsightsResourceId string = enabled ? appi.id : ''
output appInsightsConnectionString string = enabled
  ? reference(resourceId('microsoft.insights/components', appi.name), '2020-02-02').ConnectionString
  : ''
