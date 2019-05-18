param(
    # JSON Input Path
    [Parameter(Mandatory=$false,HelpMessage="Input Path of JSON file to santitize")]
    [string]
    $InputJSONPath = "..\parameters\parameters.json",
    # JSON Output Path
    [Parameter(Mandatory=$false,HelpMessage="Output path of JSON santitzed JSON file")]
    [string]
    $OutputJSONPath = "..\parameters\Skelparameters.json"
)
try{
    $InputJSON = Get-Content -Raw -Path $InputJSONPath | ConvertFrom-Json
    ##You will need to use Get-Member to decode JSON document 
}
catch{
    Write-Error -Message "Error occured during JSON Skeleton creation, please check JSON file for errors and rerun"
}
Write-Host $InputJSON