[CmdletBinding()]
param (
    # Parameter help description
    [Parameter(Mandatory=$true,HelpMessage="Build Type")]
    [ValidateSet('build','run','both')]
    [string]
    $BuildType
)
switch ($BuildType){
    "build" {
        Invoke-Expression .\Stop-Containers.ps1
        Invoke-Expression .\Remove-Containers.ps1
        Invoke-Expression .\Remove-DockerImages.ps1
        Invoke-Expression .\Build-Docker.ps1
    }
    "run" {
        Invoke-Expression .\Run-Docker.ps1
    }
    "both" {
        Invoke-Expression .\Stop-Containers.ps1
        Invoke-Expression .\Remove-Containers.ps1
        Invoke-Expression .\Remove-DockerImages.ps1
        Invoke-Expression .\Build-Docker.ps1
        Start-Process 'docker' -ArgumentList "image prune -f"
        Invoke-Expression .\Run-Docker.ps1
    }
}
##This deploys entire application


