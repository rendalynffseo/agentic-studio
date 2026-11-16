$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$projectRoot = Split-Path -Parent $PSScriptRoot
$process = Get-Process -Name 'Agentic Studio' | Where-Object { $_.Path -eq (Join-Path $projectRoot 'Agentic Studio.exe') } | Select-Object -First 1
if (-not $process) { throw 'Start the desktop app first.' }
$automation = [System.Windows.Automation.AutomationElement]
$scope = [System.Windows.Automation.TreeScope]::Descendants
$processCondition = New-Object System.Windows.Automation.PropertyCondition($automation::ProcessIdProperty, $process.Id)
$rootWindow = $automation::RootElement.FindFirst([System.Windows.Automation.TreeScope]::Children, $processCondition)
if (-not $rootWindow) { throw 'Native desktop window was not found.' }
function Find-Name($rootElement, [string]$name) {
    $condition = New-Object System.Windows.Automation.PropertyCondition($automation::NameProperty, $name)
    $element = $rootElement.FindFirst($scope, $condition)
    if (-not $element) { throw ('Missing native control: ' + $name) }
    return $element
}
function Invoke-Named($rootElement, [string]$name) {
    $element = Find-Name $rootElement $name
    $pattern = $element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
    $pattern.Invoke()
    Start-Sleep -Milliseconds 350
}
function View-State {
    $condition = New-Object System.Windows.Automation.PropertyCondition($automation::AutomationIdProperty, 'SceneViewStatus')
    $element = $rootWindow.FindFirst($scope, $condition)
    if (-not $element) { throw 'Scene view status was not found.' }
    return $element.Current.Name
}
Invoke-Named $rootWindow 'Zoom in'
if ((View-State) -notmatch 'VIEW 112%') { throw 'Zoom-in button failed.' }
Invoke-Named $rootWindow 'Reset view'
$slider = Find-Name $rootWindow 'Scene zoom percent'
$range = $slider.GetCurrentPattern([System.Windows.Automation.RangeValuePattern]::Pattern)
$range.SetValue(150)
Start-Sleep -Milliseconds 150
if ((View-State) -notmatch 'VIEW 150%') { throw 'Zoom slider failed.' }
Invoke-Named $rootWindow 'Reset view'
Invoke-Named $rootWindow 'Motion: on'
if ((View-State) -notmatch 'MOTION OFF') { throw 'Animation pause failed.' }
Invoke-Named $rootWindow 'Motion: off'
Invoke-Named $rootWindow 'Move'
if ((View-State) -notmatch 'DRAG MOVE') { throw 'Move tool failed.' }
Invoke-Named $rootWindow 'Rotate'

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class SceneMouse {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr info);
}
'@
$rootWindow.SetFocus()
$bounds = $rootWindow.Current.BoundingRectangle
$dragX = [int]($bounds.Left + 135)
$dragY = [int]($bounds.Top + 455)
function Drag-Scene([uint32]$down, [uint32]$up) {
    [SceneMouse]::SetCursorPos($dragX, $dragY) | Out-Null
    [SceneMouse]::mouse_event($down, 0, 0, 0, [UIntPtr]::Zero)
    for ($step = 1; $step -le 8; $step++) {
        [SceneMouse]::SetCursorPos(($dragX + $step * 10), ($dragY + $step * 2)) | Out-Null
        Start-Sleep -Milliseconds 25
    }
    [SceneMouse]::mouse_event($up, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 200
}
$beforeDrag = View-State
Drag-Scene 2 4
if ((View-State) -eq $beforeDrag) { throw 'Physical mouse orbit drag failed.' }
Invoke-Named $rootWindow 'Reset view'
Drag-Scene 8 16
if ((View-State) -match 'PAN 0.0 ') { throw 'Physical right-drag pan failed.' }
[SceneMouse]::SetCursorPos($dragX, $dragY) | Out-Null
[SceneMouse]::mouse_event(2048, 0, 0, 120, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 200
if ((View-State) -notmatch 'VIEW 112%') { throw 'Physical scroll-wheel zoom failed.' }
Invoke-Named $rootWindow 'Reset view'
Invoke-Named $rootWindow 'Research'
$null = Find-Name $rootWindow 'STATION / RESEARCH'
Invoke-Named $rootWindow 'All tasks'
$null = Find-Name $rootWindow 'AGENT HANDOFFS'
$jobCount = @(Get-ChildItem (Join-Path $projectRoot 'jobs') -Directory).Count
Invoke-Named $rootWindow (([char]0xff0b) + '  New task')
$dialog = Find-Name $rootWindow ('New website task ' + [char]0x2014 + ' Agentic Studio')
Invoke-Named $dialog ('Create task ' + [char]0x2197)
$null = Find-Name $dialog 'Enter a website name, business or topic, and offer.'
Invoke-Named $dialog 'Cancel'
if (@(Get-ChildItem (Join-Path $projectRoot 'jobs') -Directory).Count -ne $jobCount) { throw 'Invalid form created a job.' }
Invoke-Named $rootWindow (([char]0x25a4) + '  intake-notes.md')
$artifact = Find-Name $rootWindow ('intake-notes.md ' + [char]0x2014 + ' Agentic Studio')
$pattern = $artifact.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
$pattern.Close()
$message = 'PASS: physical mouse orbit, right-drag pan, wheel zoom, zoom buttons/slider/reset, motion toggle, drag modes, station filtering, all-task view, native task form validation/cancel, and native artifact viewer.'
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot 'ui-test-result.txt'), $message)
Write-Output $message
