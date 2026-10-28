# Token battery runner for Windows PowerShell.
#   .\run_overnight.ps1 -SelfTest                 # check the harness (fake claude, costs nothing)
#   .\run_overnight.ps1 smoke smoke-build         # first night: prove everything works
#   .\run_overnight.ps1 pilot pilot-build         # method checks on both suites
#   .\run_overnight.ps1 full full-build           # everything; re-run the same command to resume
# If scripts are blocked: powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 smoke smoke-build
param([switch]$SelfTest, [Parameter(ValueFromRemainingArguments = $true)][string[]]$Modes)

$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot
$env:PYTHONUTF8 = "1"
# Show Python's UTF-8 output correctly in this console (otherwise symbols appear as garbage).
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Find Python: the `py` launcher first, then `python`. (`python3` usually doesn't exist on Windows.)
if (Get-Command py -ErrorAction SilentlyContinue) { $Py = @("py", "-3") }
elseif (Get-Command python -ErrorAction SilentlyContinue) { $Py = @("python") }
else { Write-Error "Python 3.11+ not found. Install it from python.org and tick 'Add to PATH'."; exit 1 }
function Invoke-Py {
    # Python's output goes straight to the console; only the exit code is returned.
    param([string[]]$PyArgs)
    $pre = @($Py | Select-Object -Skip 1)
    & $Py[0] @pre @PyArgs | Out-Host
    return $LASTEXITCODE
}

if ($SelfTest) { exit (Invoke-Py @("harness/selftest.py")) }
if (-not $Modes -or $Modes.Count -eq 0) { $Modes = @("smoke") }
if (-not $env:CLAUDE_CODE_OAUTH_TOKEN) {
    Write-Error 'CLAUDE_CODE_OAUTH_TOKEN is not set. Run `claude setup-token`, then: $env:CLAUDE_CODE_OAUTH_TOKEN = "your-token"'
    exit 1
}

New-Item -ItemType Directory -Force -Path results | Out-Null
$Log = "results/overnight-$(Get-Date -Format 'yyyyMMdd-HHmm').log"
Start-Transcript -Path $Log -Append | Out-Null

# Keep the PC awake while this script runs (the screen may still turn off). Windows only.
$KeepAwake = $env:OS -eq "Windows_NT"
if ($KeepAwake) {
    Add-Type -Namespace TokenBattery -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
    $ES_CONTINUOUS = [uint32]"0x80000000"; $ES_SYSTEM_REQUIRED = [uint32]"0x00000001"
    [TokenBattery.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) | Out-Null
}

try {
    foreach ($Mode in $Modes) {
        Write-Host "== Token battery: $Mode - $(Get-Date) =="
        if ((Invoke-Py @("harness/preflight.py", "--mode", $Mode)) -ne 0) {
            Write-Host "Preflight FAILED for $Mode - see results/preflight.json"
            exit 1
        }
        $null = Invoke-Py @("harness/battery.py", "--mode", $Mode)
    }
    $null = Invoke-Py @("harness/report.py")
    Write-Host "== Done $(Get-Date). Read results/REPORT.md (and REPORT_<suite>.md, NIGHT_REPORT.md) =="
}
finally {
    $null = Invoke-Py @("harness/ponytail.py", "restore")
    if ($KeepAwake) { [TokenBattery.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null }
    Stop-Transcript | Out-Null
}
