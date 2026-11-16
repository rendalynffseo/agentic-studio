param([int]$TargetProcessId = 0)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$projectRoot = Split-Path -Parent $PSScriptRoot
$beforeBrief = [System.IO.File]::ReadAllText((Join-Path $projectRoot 'jobs/first-site/brief.json'))
$beforeState = [System.IO.File]::ReadAllText((Join-Path $projectRoot 'jobs/first-site/state.json'))
$process = if ($TargetProcessId) { Get-Process -Id $TargetProcessId } else { Get-Process -Name 'Agentic Studio' | Where-Object { $_.Path -eq (Join-Path $projectRoot 'Agentic Studio.exe') } | Select-Object -First 1 }
if (-not $process) { throw 'Start Agentic Studio first.' }
$automation = [System.Windows.Automation.AutomationElement]
$scope = [System.Windows.Automation.TreeScope]::Descendants
$processCondition = New-Object System.Windows.Automation.PropertyCondition($automation::ProcessIdProperty, $process.Id)
$rootWindow = @($automation::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children, $processCondition)) | Where-Object { $_.Current.Name -eq 'Agentic Studio' } | Select-Object -First 1
if (-not $rootWindow) { throw 'Main application window not found.' }
function Find-Name($rootElement, [string]$name) {
    $condition = New-Object System.Windows.Automation.PropertyCondition($automation::NameProperty, $name)
    $element = $rootElement.FindFirst($scope, $condition)
    if (-not $element) { throw ('Missing content control: ' + $name) }
    return $element
}
function Invoke-Named($rootElement, [string]$name) {
    (Find-Name $rootElement $name).GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
    Start-Sleep -Milliseconds 250
}
function Select-Mode($dialog, [string]$name) {
    $combo = Find-Name $dialog 'Content source'
    $combo.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
    Start-Sleep -Milliseconds 150
    $condition = New-Object System.Windows.Automation.PropertyCondition($automation::NameProperty, $name)
    $choices = $dialog.FindAll($scope, $condition)
    $selection = $null
    foreach ($choice in $choices) {
        $candidate = $null
        if ($choice.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$candidate)) { $selection = $candidate; break }
    }
    if (-not $selection) { throw ('No selectable mode item found: ' + $name) }
    $selection.Select()
    $combo.GetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern).Collapse()
    Start-Sleep -Milliseconds 150
}
$dialogCondition = New-Object System.Windows.Automation.PropertyCondition($automation::NameProperty, 'Content writer - Agentic Studio')
$dialog = $rootWindow.FindFirst($scope, $dialogCondition)
if (-not $dialog) { Invoke-Named $rootWindow 'Content writer'; $dialog = Find-Name $rootWindow 'Content writer - Agentic Studio' }
Select-Mode $dialog 'Use my exact content'
$text = Find-Name $dialog 'Exact content 1'
$value = $text.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
$sample = '  Exact ' + [char]0x201c + 'copy' + [char]0x201d + ' & <tags>.' + "`r`n" + 'Second line ' + [char]0x00e9 + '  '
$value.SetValue($sample)
if ($value.Current.Value.Replace("`r`n", "`n") -ne $sample.Replace("`r`n", "`n")) { throw 'Exact pasted wording was altered in the editor.' }
Invoke-Named $dialog 'Add content block'
$null = Find-Name $dialog 'Exact content 2'
Invoke-Named $dialog 'Remove block 2'
Select-Mode $dialog 'My content + agent fills gaps'
if ($value.Current.Value.Replace("`r`n", "`n") -ne $sample.Replace("`r`n", "`n")) { throw 'Switching modes changed the draft copy.' }
Invoke-Named $dialog 'Cancel'
if ([System.IO.File]::ReadAllText((Join-Path $projectRoot 'jobs/first-site/brief.json')) -ne $beforeBrief -or [System.IO.File]::ReadAllText((Join-Path $projectRoot 'jobs/first-site/state.json')) -ne $beforeState) { throw 'Cancel changed the existing task.' }
Invoke-Named $rootWindow (([char]0xff0b) + '  New task')
$newTask = Find-Name $rootWindow ('New website task ' + [char]0x2014 + ' Agentic Studio')
$null = Find-Name $newTask 'Content source'
Select-Mode $newTask 'Use my exact content'
$null = Find-Name $newTask 'Exact content 1'
Invoke-Named $newTask 'Cancel'
$message = 'PASS: existing-task content editor, exact Unicode/spacing paste, block add/remove, hybrid mode, cancel without task mutation, and New task content option.'
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot 'content-ui-test-result.txt'), $message)
Write-Output $message
