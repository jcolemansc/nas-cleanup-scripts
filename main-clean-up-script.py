

$date = (Get-Date).AddDays(-15)
$path = "e:\assetflow\contentstore"
$logfile = "e:\assetflow\logs\zeroed_files.log"
$savedSpaceLog = "e:\assetflow\logs\zeroed_saved_space.log"
$extensions = @(".mpg", ".mp4", ".bmp",".xml")
$dryRun = $false

if ($args -contains "-DryRun") {
    $dryRun = $true
}

$totalSize = 0
Get-ChildItem -Path $path -Recurse | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $date -and $extensions -contains $_.Extension } | ForEach-Object {
    $file = $_
    $size = $_.Length
    $fileName = $_.Name
    if (!$dryRun) {
        $stream = [System.IO.File]::Open($file.FullName, [System.IO.FileMode]::Truncate)
        $stream.SetLength(0)
        $stream.Close()
        Write-Output "Zeroed out file: $fileName with size: $size bytes"
        Add-Content -Path $logfile -Value "Zeroed out file: $fileName with size: $size bytes on $(Get-Date)"
    } else {
        Write-Output "Would have zeroed out file: $fileName with size: $size bytes"
    }
    $totalSize += $size
}

if ($totalSize -ge 1GB) {
    $totalSizeGB = [Math]::Round($totalSize / 1GB, 2)
    Write-Output "Total space saved or would be saved: $totalSizeGB GB"
    Add-Content -Path $savedSpaceLog -Value "Total space saved or would be saved: $totalSizeGB GB on $(Get-Date)"
} elseif ($totalSize -ge 1TB) {
    $totalSizeTB = [Math]::Round($totalSize / 1TB, 2)
    Write-Output "Total space saved or would be saved: $totalSizeTB TB"
    Add-Content -Path $savedSpaceLog -Value "Total space saved or would be saved: $totalSizeTB TB on $(Get-Date)"
} else {
    Write-Output "Total space saved or would be saved: $totalSize bytes"
    Add-Content -Path $savedSpaceLog -Value "Total space saved or would be saved: $totalSize bytes on $(Get-Date)"
}
