param([string]$ArchivePath = 'vendor/templates/catalog-all.zip')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$workspace = Split-Path -Parent $PSScriptRoot
$archiveFile = [System.IO.Path]::GetFullPath((Join-Path $workspace $ArchivePath))
$libraryRoot = [System.IO.Path]::GetFullPath((Join-Path $workspace 'vendor/templates/library'))
$archiveHash = (Get-FileHash -LiteralPath $archiveFile -Algorithm SHA256).Hash.ToLowerInvariant()
$versionName = 'bundle-' + $archiveHash.Substring(0, 12)
$destination = [System.IO.Path]::GetFullPath((Join-Path $libraryRoot $versionName))
if (-not $destination.StartsWith($libraryRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid library destination.' }
$archive = [System.IO.Compression.ZipFile]::OpenRead($archiveFile)
try {
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    $files = @()
    $totalBytes = 0L
    foreach ($entry in $archive.Entries) {
        $name = $entry.FullName.Replace('\', '/')
        if ($name -match '(^/|^[A-Za-z]:|(^|/)\.\.(/|$))' -or $name.Contains(':') -or (($entry.ExternalAttributes -shr 16) -band 0xf000) -eq 0xa000) { throw ('Unsafe archive entry: ' + $name) }
        $target = [System.IO.Path]::GetFullPath((Join-Path $destination $name))
        if (-not $target.StartsWith($destination + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Archive entry escaped the library.' }
        if (-not $seen.Add($name)) { throw ('Duplicate archive entry: ' + $name) }
        $totalBytes += $entry.Length
        if ($totalBytes -gt 100MB) { throw 'Template bundle exceeds the import limit.' }
        if ($name.EndsWith('/')) { continue }
        $stream = $entry.Open()
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try { $hash = ([System.BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() } finally { $sha.Dispose(); $stream.Dispose() }
        $files += @{ path = $name; length = $entry.Length; sha256 = $hash }
    }
} finally { $archive.Dispose() }
if (-not (Test-Path -LiteralPath $destination)) {
    New-Item -ItemType Directory -Force -Path $libraryRoot | Out-Null
    [System.IO.Compression.ZipFile]::ExtractToDirectory($archiveFile, $destination)
}
foreach ($file in $files) {
    $target = Join-Path $destination $file.path
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { throw ('Missing extracted file: ' + $file.path) }
    if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) { throw ('Extracted file checksum mismatch: ' + $file.path) }
}
$manifest = @{ schema_version = 1; imported_at = [DateTime]::UtcNow.ToString('o'); source_url = 'https://igaming-templates.vercel.app/downloads/iGaming_Templates_ALL.zip'; archive_path = $ArchivePath.Replace('\', '/'); archive_sha256 = $archiveHash; directory = ('vendor/templates/library/' + $versionName); files = $files }
$json = $manifest | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText((Join-Path $workspace 'vendor/templates/library-extraction.json'), $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ('Verified ' + $files.Count + ' source files from the complete template bundle. No downloaded scripts were executed.')
