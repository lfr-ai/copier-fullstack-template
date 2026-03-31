# Session Logger — SessionStart / UserPromptSubmit / Stop hook (Windows)
param()

if ($env:SKIP_LOGGING -eq "true") { exit 0 }

$LogDir = if ($env:SESSION_LOG_DIR) { $env:SESSION_LOG_DIR } else { "logs\copilot\sessions" }
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

$input_json = $input | Out-String
try { $data = $input_json | ConvertFrom-Json } catch { exit 0 }

$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$event = $data.hookEventName
$sessionId = $data.sessionId
$cwd = $data.cwd

switch ($event) {
    "SessionStart" {
        $logEntry = @{ timestamp = $timestamp; event = "session_start"; sessionId = $sessionId; cwd = $cwd } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\session.log" -Value $logEntry
        # Inject rich project context at session start
        try { $branch = git rev-parse --abbrev-ref HEAD 2>$null } catch { $branch = "unknown" }
        try { $lastCommit = git log --oneline -1 2>$null } catch { $lastCommit = "no commits" }
        try { $modifiedCount = (git diff --name-only 2>$null | Measure-Object -Line).Lines } catch { $modifiedCount = 0 }
        try { $stagedCount = (git diff --cached --name-only 2>$null | Measure-Object -Line).Lines } catch { $stagedCount = 0 }
        try { $pyVer = (python3 --version 2>$null) -replace 'Python ', '' } catch { $pyVer = "unknown" }
        try { $nodeVer = node --version 2>$null } catch { $nodeVer = "unknown" }
        $ctx = "Session audit trail: $LogDir\session.log | Branch: $branch | Last commit: $lastCommit | Modified files: $modifiedCount | Staged files: $stagedCount | Python: $pyVer | Node: $nodeVer"
        @{ hookSpecificOutput = @{ hookEventName = "SessionStart"; additionalContext = $ctx } } | ConvertTo-Json -Compress
    }
    "UserPromptSubmit" {
        if ($env:LOG_LEVEL -eq "DEBUG") {
            $logEntry = @{ timestamp = $timestamp; event = "prompt_submitted"; sessionId = $sessionId } | ConvertTo-Json -Compress
            Add-Content -Path "$LogDir\prompts.log" -Value $logEntry
        }
    }
    "Stop" {
        $logEntry = @{ timestamp = $timestamp; event = "session_end"; sessionId = $sessionId } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\session.log" -Value $logEntry
    }
    "PreCompact" {
        $trigger = if ($data.trigger) { $data.trigger } else { "unknown" }
        $logEntry = @{ timestamp = $timestamp; event = "pre_compact"; sessionId = $sessionId; trigger = $trigger } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\session.log" -Value $logEntry
    }
    "SubagentStart" {
        $agentId = $data.agent_id
        $agentType = $data.agent_type
        $logEntry = @{ timestamp = $timestamp; event = "subagent_start"; sessionId = $sessionId; agentId = $agentId; agentType = $agentType } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\session.log" -Value $logEntry
    }
    "SubagentStop" {
        $agentId = $data.agent_id
        $agentType = $data.agent_type
        $logEntry = @{ timestamp = $timestamp; event = "subagent_stop"; sessionId = $sessionId; agentId = $agentId; agentType = $agentType } | ConvertTo-Json -Compress
        Add-Content -Path "$LogDir\session.log" -Value $logEntry
    }
    { $_ -in "PreToolUse", "PostToolUse" } {
        if ($env:LOG_LEVEL -eq "DEBUG") {
            $toolName = $data.tool_name
            $logEntry = @{ timestamp = $timestamp; event = $event; sessionId = $sessionId; tool = $toolName } | ConvertTo-Json -Compress
            Add-Content -Path "$LogDir\session.log" -Value $logEntry
        }
    }
}

exit 0
