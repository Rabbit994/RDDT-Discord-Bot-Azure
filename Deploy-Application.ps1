##This deploys entire application
Invoke-Expression .\Stop-Containers.ps1
Invoke-Expression .\Remove-Containers.ps1
Invoke-Expression .\Remove-DockerImages.ps1
Invoke-Expression .\Build-Docker.ps1
Start-Process 'docker' -ArgumentList "image prune -f"
Invoke-Expression .\Run-Docker.ps1
