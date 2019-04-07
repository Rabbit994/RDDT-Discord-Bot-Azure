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
    $InputJSON = Get-Content $InputJSONPath | ConvertFrom-Json
    foreach($jsontopitem in $InputJSON){ #Pops object with top level items off
        foreach($jsonitem in $jsontopitem){ #Gets value for each object
            Write-Host $jsonitem
        }
    }
}
catch{
    Write-Error -Message "Error occured during JSON Skeleton creation, please check JSON file for errors and rerun"
}