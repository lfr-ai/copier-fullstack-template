# PreCompact Context Saver — PreCompact hook (Windows)
# Saves working state before conversation compaction.
param()

if ($env:SKIP_CONTEXT_SAVE -eq "true") { exit 0 }

$LogDir = if ($env:CONTEXT_LOG_DIR) { $env:CONTEXT_LOG_DIR } else { "logs\copilot\context" }
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$input_json = $input | Out-String
try { $data = $input_json | ConvertFrom-Json } catch { exit 0 }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$sessionId = $data.sessionId
$trigger = if ($data.trigger) { $data.trigger } else { "unknown" }
$transcriptPath = $data.transcript_path

# Collect working state
try { $branch = git rev-parse --abbrev-ref HEAD 2>$null } catch { $branch = "unknown" }
try { $modified = git diff --name-only 2>$null | Select-Object -First 20 } catch { $modified = @() }
try { $staged = git diff --cached --name-only 2>$null | Select-Object -First 20 } catch { $staged = @() }
try { $lastCommit = git log --oneline -1 2>$null } catch { $lastCommit = "no commits" }

$logEntry = @{
    timestamp = $timestamp; event = "pre_compact"; sessionId = $sessionId
    trigger = $trigger; branch = $branch
} | ConvertTo-Json -Compress
Add-Content -Path "$LogDir\compact.log" -Value $logEntry

if ($transcriptPath) {
    Add-Content -Path "$LogDir\transcripts.log" -Value "$timestamp $transcriptPath"
}

# Build context summary for the agent
$contextParts = @("Working state before compaction:", "- Branch: $branch", "- Last commit: $lastCommit")
if ($modified) { $contextParts += "- Modified files: $($modified -join ', ')" }
if ($staged) { $contextParts += "- Staged files: $($staged -join ', ')" }
$contextSummary = ($contextParts -join ' ') -replace '"', '\"'

# Output additionalContext so the agent retains working state after compaction
$output = @{
    hookSpecificOutput = @{
        hookEventName     = "PreCompact"
        additionalContext = $contextSummary
    }
} | ConvertTo-Json -Compress
Write-Output $output

exit 0
