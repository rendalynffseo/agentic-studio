param([string]$OutputName = 'Agentic Studio.exe')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$framework = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319'
$compiler = Join-Path $framework 'csc.exe'
if (-not (Test-Path -LiteralPath $compiler)) { throw 'The Windows .NET Framework compiler was not found.' }
$references = @(
    (Join-Path $framework 'WPF\PresentationFramework.dll'),
    (Join-Path $framework 'WPF\PresentationCore.dll'),
    (Join-Path $framework 'WPF\WindowsBase.dll'),
    (Join-Path $framework 'System.Xaml.dll'),
    (Join-Path $framework 'System.Web.Extensions.dll')
)
$arguments = @('/nologo', '/target:winexe', '/optimize+', '/utf8output', ('/out:' + (Join-Path $projectRoot $OutputName)))
foreach ($reference in $references) { $arguments += '/reference:' + $reference }
$arguments += @((Join-Path $PSScriptRoot 'App.cs'), (Join-Path $PSScriptRoot 'Scene.cs'), (Join-Path $PSScriptRoot 'ContentEditor.cs'))
& $compiler $arguments
if ($LASTEXITCODE -ne 0) { throw 'Desktop build failed.' }
Write-Output ('Built: ' + (Join-Path $projectRoot $OutputName))
