##Removes Containers
Start-Process 'docker' -ArgumentList "rm drblistener"
Start-Process 'docker' -ArgumentList "rm drbhandler"
Start-Process 'docker' -ArgumentList "rm drbconeremover"
Start-Process 'docker' -ArgumentList "rm drbwotupdater"
Start-Process 'docker' -ArgumentList "rm drbflasksite"