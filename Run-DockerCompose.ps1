[CmdletBinding()]
param (
    # Parameter help description
    [Parameter(Mandatory=$true,HelpMessage="Execution")]
    [ValidateSet('build','up','stop','down')]
    [string]
    $Action
)
switch($Action){
    "build" {
        Start-Process 'docker-compose' -ArgumentList 'build --no-cache --parallel' -NoNewWindow -Wait
    }
    "up" {
        Start-Process 'docker-compose' -ArgumentList 'up --detach --build' -NoNewWindow -Wait
    }
    "down" {
        Start-Process 'docker-compose' -ArgumentList 'down' -NoNewWindow -Wait
    }
    "stop" {
        Start-Process 'docker-compose' -ArgumentList 'stop' -NoNewWindow -Wait
    }
}