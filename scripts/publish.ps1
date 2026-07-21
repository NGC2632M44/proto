# One-command: sync installed skill(s) + commit + push to GitHub.
# Does NOT depend on Codex sandbox escalation -- run from your own terminal.
#
# Usage:
#   powershell scripts/publish.ps1                                   # sync Codex skill, commit, push
#   powershell scripts/publish.ps1 -Both -Message "your message"     # sync both runtimes, custom message
#   powershell scripts/publish.ps1 -SkipSync -Message "push only"    # just commit+push
param(
  [switch]$Claude,
  [switch]$Codex,
  [switch]$Both,
  [switch]$SkipSync,
  [string]$Message = "Sync proto skill and publish"
)

$ErrorActionPreference = "Stop"
$repo = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
Set-Location $repo

# 1) Sync installed skill(s) first (Codex default, unless -SkipSync)
if (-not $SkipSync) {
  $installArgs = @()
  if ($Both) { $installArgs += "-Both" } elseif ($Claude) { $installArgs += "-Claude" } else { $installArgs += "-Codex" }
  & (Join-Path $repo "scripts\install_skill.ps1") @installArgs
}

# 2) Commit local changes (skip if nothing staged)
git add -A
$status = git status --porcelain
if ($status) {
  git commit -m $Message
  if ($LASTEXITCODE -ne 0) { throw "git commit failed (exit $LASTEXITCODE)" }
} else {
  Write-Host "nothing to commit"
}

# 3) Keep history linear: rebase remote on top, then push
git pull --rebase origin main
if ($LASTEXITCODE -ne 0) { throw "git pull --rebase failed (exit $LASTEXITCODE) -- resolve conflicts then rerun with -SkipSync" }
git push origin main
if ($LASTEXITCODE -ne 0) { throw "git push failed (exit $LASTEXITCODE)" }

Write-Host ""
Write-Host "published: skill synced + pushed to GitHub (NGC2632M44/proto)"