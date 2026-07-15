param(
  [ValidateSet('quick','full','security')]
  [string]$Mode = 'quick'
)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& node (Join-Path $ScriptDir 'quality-gate.mjs') "--$Mode"
exit $LASTEXITCODE
