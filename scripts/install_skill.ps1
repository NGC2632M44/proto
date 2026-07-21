# Install/sync this proto skill into one or more runtime skill roots.
# Mirrors references/ + scripts/, overwrites SKILL.md and agents/openai.yaml.
# Excludes repo metadata (.git, LICENSE, README.md, .gitignore, COMMIT_PROTO_MSG.txt).
#
# Usage:
#   powershell scripts/install_skill.ps1                 # sync into Codex only
#   powershell scripts/install_skill.ps1 -Claude         # sync into Claude Code only
#   powershell scripts/install_skill.ps1 -Both           # sync into both
param(
  [switch]$Claude,
  [switch]$Codex,
  [switch]$Both
)

$ErrorActionPreference = "Stop"
$src = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")

$targets = @()
if ($Both) { $Codex = $true; $Claude = $true }
if (-not ($Codex -or $Claude)) { $Codex = $true }   # default: Codex
if ($Codex)   { $targets += (Join-Path $HOME ".codex\skills\proto") }
if ($Claude)  { $targets += (Join-Path $HOME ".claude\skills\proto") }

foreach ($dst in $targets) {
  if (-not (Test-Path -LiteralPath $dst)) {
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
  }
  # Mirror references/ and scripts/ (deletes stale files like references/rename.md, adds new ones)
  robocopy (Join-Path $src "references") (Join-Path $dst "references") /MIR /XD __pycache__ /NFL /NDL /NJH /NJS | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy references failed (exit $LASTEXITCODE)" }
  robocopy (Join-Path $src "scripts") (Join-Path $dst "scripts") /MIR /XD __pycache__ /NFL /NDL /NJH /NJS | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy scripts failed (exit $LASTEXITCODE)" }
  # Overwrite top-level skill files
  Copy-Item -LiteralPath (Join-Path $src "SKILL.md") -Destination (Join-Path $dst "SKILL.md") -Force
  $agentsSrc = Join-Path $src "agents\openai.yaml"
  if (Test-Path -LiteralPath $agentsSrc) {
    $agentsDst = Join-Path $dst "agents"
    if (-not (Test-Path -LiteralPath $agentsDst)) { New-Item -ItemType Directory -Force -Path $agentsDst | Out-Null }
    Copy-Item -LiteralPath $agentsSrc -Destination (Join-Path $agentsDst "openai.yaml") -Force
  }
  Write-Host "synced: $dst"
  Get-ChildItem -LiteralPath $dst -Recurse -File | Select-Object -ExpandProperty FullName
}