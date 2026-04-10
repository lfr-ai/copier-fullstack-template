# Auto-Format — PostToolUse hook (Windows)
param()

if ($env:SKIP_AUTO_FORMAT -eq "true") { exit 0 }

$input_json = $input | Out-String
try { $data = $input_json | ConvertFrom-Json } catch { exit 0 }

$toolName = $data.tool_name
$filePath = if ($data.tool_input.filePath) { $data.tool_input.filePath } elseif ($data.tool_input.file_path) { $data.tool_input.file_path } else { $null }

# Only run for file-editing tools
if ($toolName -notin @("create_file", "replace_string_in_file", "editFiles", "edit_file", "multi_replace_string_in_file")) { exit 0 }
if (-not $filePath -or -not (Test-Path $filePath)) { exit 0 }

switch -Regex ($filePath) {
    '\.py$' {
        if (Get-Command ruff -ErrorAction SilentlyContinue) {
            ruff format --quiet $filePath 2>$null
            ruff check --fix --quiet $filePath 2>$null
        }
    }
    '\.(ts|tsx|js|jsx|css|json)$' {
        if (Get-Command bunx -ErrorAction SilentlyContinue) {
            bunx biome check --write $filePath 2>$null
        }
    }
}

exit 0
