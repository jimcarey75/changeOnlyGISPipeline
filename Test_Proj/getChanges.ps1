$buildNumber="%system.build.number%"
$change_file="%system.teamcity.build.changedFiles.file%"
$deployPackagesFile="packages_to_deploy.txt"
$changeContentFile="changeContents.txt"

if (Test-Path $deployPackagesFile) {
	Remove-Item $deployPackagesFile
}
if (Test-Path $changeContentFile) {
	Remove-Item $changeContentFile
}

$change_contents = Get-Content $change_file
$change_contents >> changeContents.txt

$change_contents | %{
	$file = $_.Split(":")[0]
	$file >> changeContents.txt
	$file_extension = $file.Split(".")[-1]
	$file_extension >> changeContents.txt
    }