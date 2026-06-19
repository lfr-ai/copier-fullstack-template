// ── Azure App Service (Linux Container) ──────────────────────────
//
// Deploys an App Service Plan + Web App configured for Linux
// container workloads, with managed identity for ACR pull and
// Key Vault access.

@description('Prefix used for resource names (e.g., myapp-dev)')
param namePrefix string

@description('Location for the App Service. Default: resource group location')
param location string = resourceGroup().location

@description('Optional App Service Plan name')
param planName string = ''

@description('Optional Web App name')
param appName string = ''

@description('App Service Plan SKU')
@allowed(['B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'P1v3', 'P2v3', 'P3v3'])
param skuName string = 'B1'

@description('ACR login server for container image pull')
param acrLoginServer string = ''

@description('Container image name (without registry prefix)')
param containerImage string = ''

@description('Container image tag')
param containerTag string = 'latest'

@description('App settings (environment variables)')
param appSettings array = []

@description('Health check path')
param healthCheckPath string = '/health'

@description('Always On (keeps app warm)')
param alwaysOn bool = true

@description('Minimum TLS version')
@allowed(['1.2', '1.3'])
param minTlsVersion string = '1.2'

@description('Enable auto-scale (requires Standard+ SKU)')
param enableAutoScale bool = false

@description('Auto-scale minimum instances')
@minValue(1)
@maxValue(10)
param autoScaleMinInstances int = 1

@description('Auto-scale maximum instances')
@minValue(1)
@maxValue(30)
param autoScaleMaxInstances int = 3

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

// ── Derived values ───────────────────────────────────────────────

var aspName = empty(planName) ? '${namePrefix}-plan' : planName
var webAppName = empty(appName) ? '${namePrefix}-app' : appName
var fullImageName = !empty(acrLoginServer) && !empty(containerImage)
  ? '${acrLoginServer}/${containerImage}:${containerTag}'
  : ''

// ── App Service Plan ─────────────────────────────────────────────

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = if (enabled) {
  name: aspName
  location: location
  kind: 'linux'
  sku: {
    name: skuName
  }
  properties: {
    reserved: true // Required for Linux
  }
  tags: tags
}

// ── Web App ──────────────────────────────────────────────────────

resource webApp 'Microsoft.Web/sites@2023-12-01' = if (enabled) {
  name: webAppName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: !empty(fullImageName) ? 'DOCKER|${fullImageName}' : ''
      alwaysOn: alwaysOn
      minTlsVersion: minTlsVersion
      healthCheckPath: healthCheckPath
      httpLoggingEnabled: true
      detailedErrorLoggingEnabled: true
      acrUseManagedIdentityCreds: !empty(acrLoginServer)
      appSettings: concat(appSettings, [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'DOCKER_ENABLE_CI'
          value: 'true'
        }
      ])
    }
  }
  tags: tags
}

// ── Auto-scale settings ──────────────────────────────────────────

resource autoScale 'Microsoft.Insights/autoscalesettings@2022-10-01' = if (enabled && enableAutoScale) {
  name: '${webAppName}-autoscale'
  location: location
  properties: {
    enabled: true
    targetResourceUri: plan.id
    profiles: [
      {
        name: 'Auto Scale Profile'
        capacity: {
          minimum: string(autoScaleMinInstances)
          maximum: string(autoScaleMaxInstances)
          default: string(autoScaleMinInstances)
        }
        rules: [
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: plan.id
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT5M'
              timeAggregation: 'Average'
              operator: 'GreaterThan'
              threshold: 70
            }
            scaleAction: {
              direction: 'Increase'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT5M'
            }
          }
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: plan.id
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT10M'
              timeAggregation: 'Average'
              operator: 'LessThan'
              threshold: 30
            }
            scaleAction: {
              direction: 'Decrease'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT10M'
            }
          }
        ]
      }
    ]
  }
  tags: tags
}

// ── Outputs ──────────────────────────────────────────────────────

output appServiceName string = enabled ? webApp.name : ''
output appServiceHostname string = enabled ? webApp.properties.defaultHostName : ''
output appServiceResourceId string = enabled ? webApp.id : ''
output appServicePrincipalId string = enabled ? webApp.identity.principalId : ''
output planResourceId string = enabled ? plan.id : ''
