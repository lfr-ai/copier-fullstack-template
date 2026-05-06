# Blocks destructive bash commands before execution.
# Reads JSON tool input from stdin, checks command against dangerous patterns.
param()
$ErrorActionPreference = "Stop"

try {
    $rawInput = $input -join "`n"
    $inputData = $rawInput | ConvertFrom-Json -ErrorAction Stop
    $cmd = $inputData.command
} catch {
    exit 0
}

if ([string]::IsNullOrWhiteSpace($cmd)) {
    exit 0
}

$dangerousPatterns = @(
    "rm -rf /",
    "rm -rf ~",
    "rm -rf *",
    "git push --force",
    "git push -f ",
    "git reset --hard",
    "git clean -f",
    "git clean -fd",
    "git clean -fx",
    "DROP TABLE",
    "DROP DATABASE",
    "--no-verify",
    "| bash",
    "| sh",
    "mkfs",
    "dd if="
)

foreach ($pattern in $dangerousPatterns) {
    if ($cmd.ToLower().Contains($pattern.ToLower())) {
        @{
            decision = "block"
            reason   = "Blocked: matches destructive pattern '$pattern'. Confirm manually if intentional."
        } | ConvertTo-Json -Compress
        exit 0
    }
}

exit 0
