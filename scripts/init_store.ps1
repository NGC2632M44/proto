# One-command: create the canonical protocol store and link runtimes onto it.
# Idempotent. Safe: writes only to $PROTO_STORE (default ~/.protocols) and
# junctions the exact <runtime>/proto/references/protocols path.
#
# Usage:
#   powershell scripts/init_store.ps1 -Both            # store + link cc and codex
#   powershell scripts/init_store.ps1 -Codex -NoLink  # just build the store
param(
  [switch]$Codex,
  [switch]$Claude,
  [switch]$Both,
  [switch]$NoLink
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$store = $env:PROTO_STORE
if (-not $store) { $store = Join-Path $HOME ".protocols" }
$protoDir = Join-Path $store "protocols"
$inboxDir = Join-Path $store "inbox"

New-Item -ItemType Directory -Force -Path $protoDir, $inboxDir | Out-Null
# Mirror the repo's protocols into the store (store becomes the shared fuel source)
robocopy (Join-Path $repo "references\protocols") $protoDir /MIR /XD __pycache__ /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy to store failed ($LASTEXITCODE)" }

# Git-init the store for optional cross-machine sync (user adds a remote later)
if (-not (Test-Path (Join-Path $store ".git"))) { git -C $store init --quiet 2>&1 | Out-Null }
$gitignore = Join-Path $store ".gitignore"
if (-not (Test-Path -LiteralPath $gitignore)) {
  "inbox/" | Set-Content -LiteralPath $gitignore -Encoding UTF8
}
git -C $store add -- protocols 2>&1 | Out-Null
Write-Host "store ready: $store ($((Get-ChildItem $protoDir -File).Count) protocol files)"

if ($NoLink) { return }

# Link runtimes onto the store
$linkArgs = @()
if ($Both) { $linkArgs += "-Both" }
elseif ($Claude) { $linkArgs += "-Claude" }
else { $linkArgs += "-Codex" }
& (Join-Path $repo "scripts\link_store.ps1") @linkArgs