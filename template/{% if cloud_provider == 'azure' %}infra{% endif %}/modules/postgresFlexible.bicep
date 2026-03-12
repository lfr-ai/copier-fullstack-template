// ── Azure Database for PostgreSQL Flexible Server ──────────────────

@description('Prefix used for resource names')
param namePrefix string

@description('Location for the server. Default: resource group location')
param location string = resourceGroup().location

@description('Optional server name')
param serverName string = ''

@description('SKU name (e.g., Standard_B1ms, Standard_D2ds_v4)')
param skuName string = 'Standard_B1ms'

@description('SKU tier')
@allowed(['Burstable', 'GeneralPurpose', 'MemoryOptimized'])
param skuTier string = 'Burstable'

@description('PostgreSQL major version')
@allowed(['14', '15', '16', '17'])
param version string = '17'

@description('Storage size in GB')
@minValue(32)
@maxValue(16384)
param storageSizeGB int = 32

@description('Administrator login name')
param administratorLogin string = 'pgadmin'

@secure()
@description('Administrator login password')
param administratorLoginPassword string

@description('High availability mode')
@allowed(['Disabled', 'SameZone', 'ZoneRedundant'])
param highAvailabilityMode string = 'Disabled'

@description('Backup retention period in days')
@minValue(7)
@maxValue(35)
param backupRetentionDays int = 7

@description('Geo-redundant backup')
@allowed(['Enabled', 'Disabled'])
param geoRedundantBackup string = 'Disabled'

@description('Public network access')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

@description('Tags to apply')
param tags object = {}

@description('Enable deployment of this module. Default: true')
param enabled bool = true

var pgName = empty(serverName) ? '${namePrefix}-psql' : serverName

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = if (enabled) {
  name: pgName
  location: location
  sku: {
    name: skuName
    tier: skuTier
  }
  properties: {
    version: version
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    storage: {
      storageSizeGB: storageSizeGB
    }
    backup: {
      backupRetentionDays: backupRetentionDays
      geoRedundantBackup: geoRedundantBackup
    }
    highAvailability: {
      mode: highAvailabilityMode
    }
    network: {
      publicNetworkAccess: publicNetworkAccess
    }
    maintenanceWindow: {
      customWindow: 'Enabled'
      dayOfWeek: 0
      startHour: 2
      startMinute: 0
    }
  }
  tags: tags
}

// Allow Azure services to access the server
resource allowAzureServices 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2024-08-01' = if (enabled && publicNetworkAccess == 'Enabled') {
  parent: postgres
  name: 'AllowAllAzureServicesAndResourcesWithinAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Enable pgvector extension
resource pgvectorExtension 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2024-08-01' = if (enabled) {
  parent: postgres
  name: 'azure.extensions'
  properties: {
    value: 'VECTOR,UUID-OSSP,PGCRYPTO'
    source: 'user-override'
  }
}

output serverName string = enabled ? postgres.name : ''
output serverFqdn string = enabled ? postgres.properties.fullyQualifiedDomainName : ''
output serverResourceId string = enabled ? postgres.id : ''
