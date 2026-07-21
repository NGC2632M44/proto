# Auto-capture shell hook for proto (Windows PowerShell 5.1+).
# Records a failed command into $PROTO_STORE/inbox via collect_trace.py.
# Mechanism: custom `prompt` function inspects $LASTEXITCODE before each
# prompt; on nonzero exit it reads the latest history line and calls
# collect_trace.py. No PSReadLine key handler (avoids fragile param binding).
#
# Usage:
#   powershell scripts/auto_capture_hook.ps1             # install into $PROFILE
#   powershell scripts/auto_capture_hook.ps1 -Uninstall  # remove
param([switch]$Uninstall)

$ErrorActionPreference = "Stop"
$marker = "# >>> proto-auto-capture >>>"
$endmark = "# <<< proto-auto-capture <<<"
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path -Parent $profilePath
if (-not (Test-Path -LiteralPath $profileDir)) { New-Item -ItemType Directory -Force -Path $profileDir | Out-Null }
if (-not (Test-Path -LiteralPath $profilePath)) { New-Item -ItemType File -Force -Path $profilePath | Out-Null }

# The profile snippet, written as single-quoted lines joined by newlines so
# nothing is pre-expanded. Tokens like PROTO_STORE_PLACEHOLDER are replaced
# with literal $-expressions after assembly.
$lines = @(
  'if (-not $env:PROTO_STORE) { $env:PROTO_STORE = Join-Path $HOME ".protocols" }',
  'function global:prompt {',
  '  $exit = $LASTEXITCODE',
  '  if ($null -ne $exit -and $exit -ne 0) {',
  '    $cmd = $null',
  '    try { $hist = Get-History -Count 1; if ($hist) { $cmd = $hist.CommandLine } } catch {}',
  '    if ($cmd -and $cmd -notmatch ''^(cd|exit|clear|cls|ls|dir|pwd|set|echo|git status|git log)'') {',
  '      $collector = Join-Path $HOME ".codex\skills\proto\scripts\collect_trace.py"',
  '      if (-not (Test-Path $collector)) { $collector = Join-Path $HOME ".claude\skills\proto\scripts\collect_trace.py" }',
  '      if ((Test-Path $collector) -and (Get-Command python -ErrorAction SilentlyContinue)) {',
  '        try { & python $collector $cmd --exit $exit --runtime powershell 2>$null | Out-Null } catch {}',
  '      }',
  '    }',
  '  }',
  '  "PS " + $executionContext.SessionState.Path.CurrentLocation + (">" * ($nestedPromptLevel + 1)) + " "',
  '}'
)
$snippet = ($lines -join "`r`n")
$block = $marker + "`r`n" + $snippet + "`r`n" + $endmark

if ($Uninstall) {
  $content = Get-Content -LiteralPath $profilePath -Raw -ErrorAction SilentlyContinue
  if ($content -and $content.Contains($marker)) {
    $pattern = "(?s)\r?\n?" + [regex]::Escape($marker) + ".*" + [regex]::Escape($endmark) + "\r?\n?"
    $new = [regex]::Replace($content, $pattern, '')
    Set-Content -LiteralPath $profilePath -Value $new -Encoding UTF8
    Write-Host "removed proto auto-capture hook from $profilePath"
  } else {
    Write-Host "no hook found in $profilePath"
  }
  return
}

$content = Get-Content -LiteralPath $profilePath -Raw -ErrorAction SilentlyContinue
if ($content -and $content.Contains($marker)) {
  Write-Host "proto auto-capture hook already present in $profilePath"
  return
}
Add-Content -LiteralPath $profilePath -Value $block -Encoding UTF8
Write-Host "installed proto auto-capture hook into $profilePath"
Write-Host "reload with: . $PROFILE  (or open a new terminal)"