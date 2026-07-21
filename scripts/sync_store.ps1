# Mount the canonical protocol store into each detected runtime skill folder.
# Default store: $PROTO_STORE or ~/.protocols. Uses junctions (no admin needed).
#
# Usage:
#   pwsh scripts/sync_store.ps1            # link both runtimes
#   pwsh scripts/sync_store.ps1 -Pull     # git pull the store first
#   pwsh scripts/sync_store.ps1 -Push     # git commit + push the store after
param(
  [switch]$Pull,
  [switch]$Push,
  [string]$Store = $(if ($env:PROTO_STORE) { $env:PROTO_STORE } else { Join-Path $HOME ".protocols" })
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Store)) {
  New-Item -ItemType Directory -Force -Path $Store | Out-Null
}
$storeP = (Resolve-Path -LiteralPath $Store).Path
$protoDir = Join-Path $storeP "protocols"
$inboxDir = Join-Path $storeP "inbox"
New-Item -ItemType Directory -Force -Path $protoDir, $inboxDir | Out-Null

if ($Pull -and (Test-Path -LiteralPath (Join-Path $storeP ".git"))) {
  git -C $storeP pull --ff-only
}

$runtimes = @(
  @{ Name = "claude-code"; Skill = (Join-Path $HOME ".claude\skills\proto") },
  @{ Name = "codex";       Skill = (Join-Path $HOME ".codex\skills\proto") }
)

foreach ($rt in $runtimes) {
  $skill = $rt.Skill
  if (-not (Test-Path -LiteralPath $skill)) {
    Write-Host "skip $($rt.Name): skill folder not installed at $skill"
    continue
  }
  $refDir = Join-Path $skill "references"
  New-Item -ItemType Directory -Force -Path $refDir | Out-Null
  $link = Join-Path $refDir "protocols"
  if (Test-Path -LiteralPath $link) {
    $item = Get-Item -LiteralPath $link
    if ($item.LinkType -in "Junction","SymbolicLink") {
      $item.Delete()
    } else {
      Write-Host "skip $($rt.Name): $link is a real folder (will not overwrite)"
      continue
    }
  }
  New-Item -ItemType Junction -Path $link -Target $protoDir | Out-Null
  Write-Host "linked $($rt.Name): $link -> $protoDir"
}

if ($Push -and (Test-Path -LiteralPath (Join-Path $storeP ".git"))) {
  git -C $storeP add -A
  git -C $storeP commit -m "sync protocols" 2>$null
  git -C $storeP push
}
