$date1Year = (Get-Date).AddDays(-365)
$date6Months = (Get-Date).AddDays(-183)
$path = "e:\assetflow\contentstore"
$logfile = "e:\assetflow\logs\zeroed_files.log"
$zeroedSavedSpaceLog = "e:\assetflow\logs\zeroed_saved_space.log"
$extensions = @(".mpg", ".mp4", ".bmp",".xml")

# Check if the script is run in dry-run mode or not
$dryRun = $false
if ($args -eq "dryrun") {
    $dryRun = $true
}

# Zero out files older than 1 year or 6 months
$totalSavedSpace1Year = 0
$totalSavedSpace6Months = 0
Get-ChildItem -Path $path -Recurse | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $date1Year -and $extensions -contains $_.Extension } | ForEach-Object {
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
        Write-Output "Dry run: would have zeroed out file: $fileName with size: $size bytes"
    }
    $totalSavedSpace1Year += $size
}
Get-ChildItem -Path $path -Recurse | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $date6Months -and $_.LastWriteTime -gt $date1Year -and $extensions -contains $_.Extension } | ForEach-Object {
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
        Write-Output "Dry run: would have zeroed out file: $fileName with size: $size bytes"
    }
    $totalSavedSpace6Months += $size
}

$gb6Months = [Math]::Round($totalSavedSpace6Months / 1GB, 2)
$tb6Months = [Math]::Round($totalSavedSpace6Months / 1TB, 2)

Write-Output "Total saved space in GB for files older than 6 months: $gb6Months"
Write-Output "Total saved space in TB for files older than 6 months: $tb6Months"

Add-Content -Path "e:\assetflow\logs\zeroed_saved_space.log" -Value "Total saved space in GB for files older than 6 months: $gb6Months on $(Get-Date)"
Add-Content -Path "e:\assetflow\logs\zeroed_saved_space.log" -Value "Total saved space in TB for files older than 6 months: $tb6Months on $(Get-Date)"

$gb1Year = [Math]::Round($totalSavedSpace1Year / 1GB, 2)
$tb1Year = [Math]::Round($totalSavedSpace1Year / 1TB, 2)

Write-Output "Total saved space in GB for files older than 1 year: $gb1Year"
Write-Output "Total saved space in TB for files older than 1 year: $tb1Year"

Add-Content -Path "e:\assetflow\logs\zeroed_saved_space.log" -Value "Total saved space in GB for files older than 1 year: $gb1Year on $(Get-Date)"
Add-Content -Path "e:\assetflow\logs\zeroed_saved_space.log" -Value "Total saved space in TB for files older than 1 year: $tb1Year on $(Get-Date)"
