param([Parameter(Mandatory=$true)][int]$TargetProcessId)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$deadline = (Get-Date).AddSeconds(30)
$window = $null
do {
    $target = Get-Process -Id $TargetProcessId
    if ($target.MainWindowHandle -ne 0) { $window = [System.Windows.Automation.AutomationElement]::FromHandle($target.MainWindowHandle) }
    if (-not $window) { Start-Sleep -Milliseconds 200 }
} until ($window -or (Get-Date) -gt $deadline)
if (-not $window) { throw 'The app window did not become available.' }
$ai = $window.FindFirst([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'AI'))
if (-not $ai) { throw 'AI worker button is missing.' }
$ai.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
$panel = $null
do {
    $panel = $window.FindFirst([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'AI worker - Agentic Studio'))
    if (-not $panel) { $panel = [System.Windows.Automation.AutomationElement]::RootElement.FindFirst([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'AI worker - Agentic Studio')) }
    if (-not $panel) { Start-Sleep -Milliseconds 200 }
} until ($panel -or (Get-Date) -gt $deadline)
if (-not $panel) { throw 'Native AI worker window did not open.' }
$ready = $false
do {
    $texts = $panel.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::ControlTypeProperty, [System.Windows.Automation.ControlType]::Text))
    foreach ($text in $texts) { if ($text.Current.Name -like 'Connected - your account is ready.*') { $ready = $true } }
    if (-not $ready) { Start-Sleep -Milliseconds 200 }
} until ($ready -or (Get-Date) -gt $deadline)
if (-not $ready) { throw 'The native worker did not confirm the signed-in account.' }
$advanced = $panel.FindFirst([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, 'Advanced settings & recovery'))
if ($advanced) { $advanced.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand() }
foreach ($label in @('Start / continue', 'Pause after current agent', 'Stop worker', 'Choose engine', 'Check connection', 'Recover interrupted stage', 'AI worker live log')) {
    $element = $panel.FindFirst([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.PropertyCondition]::new([System.Windows.Automation.AutomationElement]::NameProperty, $label))
    if (-not $element) { throw ('Missing native worker control: ' + $label) }
}
$result = 'PASS: native AI button opens worker panel; installed Codex account is signed in; Start, pause, stop, sign-in, engine selection, recovery and live-log controls are present. No task was started or changed.'
Set-Content -LiteralPath (Join-Path $PSScriptRoot 'worker-ui-test-result.txt') -Value $result
Write-Output $result
