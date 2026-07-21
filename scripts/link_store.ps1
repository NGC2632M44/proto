# Link each runtime's proto skill references/protocols onto the canonical store.
# Safe-by-design: only acts on the exact path <runtime>/proto/references/protocols;
# verifies each target resolves under a "proto" skill folder before touching it.
#
# Usage:
#   powershell scripts/link_store.ps1 -Both
#   powershell scripts/link_store.ps1 -Codex
param(
  [switch]$Codex,
  [switch]$Claude,
  [switch]$Both
)

$ErrorActionPreference = "Stop"
$store = $env:PROTO_STORE
if (-not $store) { $store = Join-Path $HOME ".protocols" }
$protoDir = Join-Path $store "protocols"
if (-not (Test-Path -LiteralPath $protoDir)) {
  throw "Store protocols dir not found: $protoDir (run init_store.ps1 first)"
}

$targets = @()
if ($Both) { $Codex = $true; $Claude = $true }
if ($Codex)  { $targets += (Join-Path $HOME ".codex\skills\proto") }
if ($Claude) { $targets += (Join-Path $HOME ".claude\skills\proto") }
if (-not ($Codex -or $Claude)) { $Codex = $true; $targets += (Join-Path $HOME ".codex\skills\proto") }

foreach ($skill in $targets) {
  if (-not (Test-Path -LiteralPath $skill)) { Write-Host "skip $skill : not installed"; continue }
  # safety: skill path must end in a proto skill folder
  if (-not ($skill -match "[\\/]proto$")) { throw "refusing to touch unexpected path: $skill" }
  $refDir = Join-Path $skill "references"
  if (-not (Test-Path -LiteralPath $refDir)) { New-Item -ItemType Directory -Force -Path $refDir | Out-Null }
  $link = Join-Path $refDir "protocols"

  if (Test-Path -LiteralPath $link) {
    $item = Get-Item -LiteralPath $link
    if ($item.PSIsContainer -and ($item.LinkType -in "Junction","SymbolicLink")) {
      $item.Delete()
    } elseif ($item.PSIsContainer) {
      # real folder: its contents are mirrored in the store + repo, so safe to remove
      Remove-Item -LiteralPath $link -Recurse -Force
    } else {
      throw "refusing to replace non-directory: $link"
    }
  }
  New-Item -ItemType Junction -Path $link -Target $protoDir | Out-Null
  Write-Host "linked: $link -> $protoDir"
}