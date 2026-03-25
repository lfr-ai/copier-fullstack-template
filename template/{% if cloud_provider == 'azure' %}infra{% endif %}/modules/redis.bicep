// ── Azure Cache for Redis ─────────────────────────────────────────
//
// Supports Basic, Standard, and Premium tiers with security hardening,
// diagnostics, patching, firewall, persistence, availability zones,
// clustering, and Microsoft Entra authentication.
//
// API reference: https://learn.microsoft.com/azure/templates/microsoft.cache/redis

// ── Parameters ───────────────────────────────────────────────────

@description('Prefix used for resource names (e.g., myapp-dev)')
param namePrefix string

@description('Location for the Redis cache. Default: resource group location')
param location string = resourceGroup().location

@description('Optional Redis cache name override. If empty, derived as {namePrefix}-redis')
param cacheName string = ''

// ── SKU ──────────────────────────────────────────────────────────

@description('SKU name. Basic = no SLA/replication. Standard = SLA + replication. Premium = clustering, zones, persistence, VNet.')
@allowed(['Basic', 'Standard', 'Premium'])
param skuName string = 'Basic'

@description('SKU family. C = Basic/Standard, P = Premium.')
@allowed(['C', 'P'])
param skuFamily string = 'C'

@description('Cache capacity. 0–6 for C family (250 MB–53 GB), 1–5 for P family (6–120 GB).')
@minValue(0)
@maxValue(6)
param skuCapacity int = 0

// ── Version & TLS ────────────────────────────────────────────────

@description('Redis engine version. 6 = Redis 6.x LTS. Default: 6')
@allowed(['6'])
param redisVersion string = '6'

@description('Minimum TLS version for client connections. Default: 1.2 (required for PCI-DSS)')
@allowed(['1.2'])
param minimumTlsVersion string = '1.2'

@description('Enable legacy non-SSL port 6379. MUST be false for production workloads.')
param enableNonSslPort bool = false

// ── Networking ───────────────────────────────────────────────────

@description('Public network access. Set to Disabled when using Private Endpoints.')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

// ── Authentication ───────────────────────────────────────────────

@description('Disable access-key (shared-key) authentication. When true, only Microsoft Entra (AAD) tokens are accepted. Requires enableEntraAuth = true.')
param disableAccessKeyAuthentication bool = false

@description('Enable Microsoft Entra ID (AAD) authentication for data-plane access. Recommended for zero-trust architectures.')
param enableEntraAuth bool = false

// ── Identity ─────────────────────────────────────────────────────

@description('Enable system-assigned managed identity on the Redis cache (required for Entra auth, Key Vault references, diagnostic sinks).')
param enableManagedIdentity bool = false

// ── Update channel ───────────────────────────────────────────────

@description('Update channel controls how quickly Redis engine patches are applied. Stable = default cadence. Preview = early access.')
@allowed(['Stable', 'Preview'])
param updateChannel string = 'Stable'

// ── Redis configuration ──────────────────────────────────────────

@description('Eviction policy when max memory is reached. allkeys-lru is the safest default for caching workloads.')
@allowed([
  'volatile-lru'
  'allkeys-lru'
  'volatile-lfu'
  'allkeys-lfu'
  'volatile-random'
  'allkeys-random'
  'volatile-ttl'
  'noeviction'
])
param maxMemoryPolicy string = 'allkeys-lru'

@description('Memory (MB) reserved for non-cache operations such as replication and AOF. Recommended: ≥10 % of cache size for Standard/Premium.')
param maxMemoryDelta string = ''

@description('Memory (MB) reserved for fragmentation. Recommended: ≥10 % for workloads with heavy write churn.')
param maxFragmentationMemoryReserved string = ''

@description('Enable keyspace notifications (e.g., "Kex" for key-event expiration). Empty string = disabled.')
param notifyKeyspaceEvents string = ''

// ── Premium-tier: Availability zones ─────────────────────────────

@description('Availability zones for zone-redundant deployment (Premium only). E.g., ["1", "2", "3"]. Empty = no zone pinning.')
param zones array = []

// ── Premium-tier: Clustering ─────────────────────────────────────

@description('Number of shards in a Premium cluster. 0 = no clustering. 1–10 for clustered cache. Premium only.')
@minValue(0)
@maxValue(10)
param shardCount int = 0

@description('Number of read replicas per primary shard (Premium only). 0 = no extra replicas beyond the built-in replica.')
@minValue(0)
@maxValue(3)
param replicasPerPrimary int = 0

// ── Premium-tier: Persistence ────────────────────────────────────

@description('Enable RDB persistence (point-in-time snapshots). Premium only.')
param enableRdbPersistence bool = false

@description('RDB snapshot frequency in seconds. 900 = 15 min, 3600 = 1 h, 86400 = 24 h. Premium only.')
@allowed([900, 3600, 86400])
param rdbBackupFrequencyInSeconds int = 3600

@description('Enable AOF persistence (append-only file) for near-zero data loss. Premium only. Cannot be combined with RDB on the same cache.')
param enableAofPersistence bool = false

// ── Patch schedule ───────────────────────────────────────────────

@description('Day of week for the maintenance/patch window (Standard + Premium). Empty = Azure-managed schedule.')
@allowed(['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Everyday', 'Weekend'])
param patchScheduleDayOfWeek string = ''

@description('Start hour (UTC, 0–23) for the maintenance window.')
@minValue(0)
@maxValue(23)
param patchScheduleStartHourUtc int = 2

@description('Optional ISO-8601 duration for the patch window (e.g., "PT5H"). Empty = default duration.')
param patchScheduleMaintenanceWindow string = ''

// ── Firewall rules ───────────────────────────────────────────────

@description('Array of firewall rules. Each entry: { name: string, startIP: string, endIP: string }. Applied only when publicNetworkAccess = Enabled.')
param firewallRules array = []

// ── Diagnostics ──────────────────────────────────────────────────

@description('Enable diagnostic settings (metrics + logs → Log Analytics). Requires logAnalyticsWorkspaceId.')
param enableDiagnostics bool = false

@description('Resource ID of the Log Analytics workspace for diagnostic data.')
param logAnalyticsWorkspaceId string = ''

// ── Tags & feature flag ──────────────────────────────────────────

@description('Tags to apply to all resources in this module')
param tags object = {}

@description('Enable deployment of this module. When false, all resources are skipped.')
param enabled bool = true

// ── Derived values ───────────────────────────────────────────────

var redisName = empty(cacheName) ? '${namePrefix}-redis' : cacheName
var isPremium = skuName == 'Premium'
var isBasic = skuName == 'Basic'

// Build the redisConfiguration object dynamically based on provided params
var baseRedisConfig = {
  'maxmemory-policy': maxMemoryPolicy
}

var deltaConfig = empty(maxMemoryDelta)
  ? {}
  : {
      'maxmemory-delta': maxMemoryDelta
    }

var fragConfig = empty(maxFragmentationMemoryReserved)
  ? {}
  : {
      'maxfragmentationmemory-reserved': maxFragmentationMemoryReserved
    }

var notifyConfig = empty(notifyKeyspaceEvents)
  ? {}
  : {
      'notify-keyspace-events': notifyKeyspaceEvents
    }

// RDB persistence config (Premium only)
var rdbConfig = (isPremium && enableRdbPersistence)
  ? {
      'rdb-backup-enabled': 'true'
      'rdb-backup-frequency': string(rdbBackupFrequencyInSeconds)
    }
  : {}

// AOF persistence config (Premium only)
var aofConfig = (isPremium && enableAofPersistence)
  ? {
      'aof-backup-enabled': 'true'
    }
  : {}

var redisConfiguration = union(baseRedisConfig, deltaConfig, fragConfig, notifyConfig, rdbConfig, aofConfig)

// ── Main resource ────────────────────────────────────────────────

resource redisCache 'Microsoft.Cache/redis@2024-11-01' = if (enabled) {
  name: redisName
  location: location
  zones: (isPremium && !empty(zones)) ? zones : []
  identity: enableManagedIdentity
    ? {
        type: 'SystemAssigned'
      }
    : null
  properties: {
    sku: {
      name: skuName
      family: skuFamily
      capacity: skuCapacity
    }
    enableNonSslPort: enableNonSslPort
    minimumTlsVersion: minimumTlsVersion
    redisVersion: redisVersion
    publicNetworkAccess: publicNetworkAccess
    disableAccessKeyAuthentication: disableAccessKeyAuthentication
    redisConfiguration: redisConfiguration
    replicasPerMaster: isPremium ? replicasPerPrimary : null
    shardCount: isPremium ? shardCount : null
    updateChannel: updateChannel
  }
  tags: tags
}

// ── Microsoft Entra (AAD) authentication ─────────────────────────
// Creates a built-in access policy that allows AAD-token–based connections.
// Requires the connecting principal to hold the "Redis Cache Contributor"
// or a custom data-plane RBAC role.

resource entraAccessPolicy 'Microsoft.Cache/redis/accessPolicyAssignments@2024-11-01' = if (enabled && enableEntraAuth && enableManagedIdentity) {
  parent: redisCache
  name: 'entra-system-identity'
  properties: {
    accessPolicyName: 'Data Owner'
    objectId: redisCache.identity.principalId
    objectIdAlias: '${redisName}-system-identity'
  }
}

// ── Patch schedule ───────────────────────────────────────────────
// Standard and Premium tiers support scheduled maintenance windows.

resource patchSchedule 'Microsoft.Cache/redis/patchSchedules@2024-11-01' = if (enabled && !isBasic && !empty(patchScheduleDayOfWeek)) {
  parent: redisCache
  name: 'default'
  properties: {
    scheduleEntries: [
      union(
        {
          dayOfWeek: patchScheduleDayOfWeek
          startHourUtc: patchScheduleStartHourUtc
        },
        empty(patchScheduleMaintenanceWindow)
          ? {}
          : {
              maintenanceWindow: patchScheduleMaintenanceWindow
            }
      )
    ]
  }
}

// ── Firewall rules ───────────────────────────────────────────────
// Applied only when publicNetworkAccess is Enabled.

@batchSize(1)
resource firewallRule 'Microsoft.Cache/redis/firewallRules@2024-11-01' = [
  for (rule, i) in firewallRules: if (enabled && publicNetworkAccess == 'Enabled' && !empty(firewallRules)) {
    parent: redisCache
    name: rule.name
    properties: {
      startIP: rule.startIP
      endIP: rule.endIP
    }
  }
]

// ── Diagnostic settings ──────────────────────────────────────────
// Streams Redis metrics and connection logs to Log Analytics for
// monitoring, alerting, and cost-optimisation dashboards.

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enabled && enableDiagnostics && !empty(logAnalyticsWorkspaceId)) {
  name: '${redisName}-diag'
  scope: redisCache
  properties: {
    workspaceId: logAnalyticsWorkspaceId
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          enabled: false
          days: 0
        }
      }
    ]
    logs: [
      {
        categoryGroup: 'allLogs'
        enabled: true
        retentionPolicy: {
          enabled: false
          days: 0
        }
      }
    ]
  }
}

// ── Outputs ──────────────────────────────────────────────────────

@description('Name of the deployed Redis cache')
output redisCacheName string = enabled ? redisCache.name : ''

@description('Hostname for SSL connections (e.g., myapp-dev-redis.redis.cache.windows.net)')
output redisCacheHostName string = enabled ? redisCache.properties.hostName : ''

@description('SSL port (default 6380)')
output redisCachePort int = enabled ? redisCache.properties.sslPort : 0

@description('Full resource ID of the Redis cache')
output redisCacheResourceId string = enabled ? redisCache.id : ''

@description('Whether access-key authentication is available (does NOT output the key itself)')
output redisAccessKeysEnabled bool = enabled && !disableAccessKeyAuthentication

@description('System-assigned managed identity principal ID (empty if not enabled)')
output redisManagedIdentityPrincipalId string = (enabled && enableManagedIdentity)
  ? redisCache.identity.principalId
  : ''
