##Removes Containers
Start-Process 'docker' -NoNewWindow -ArgumentList "rm drblistener"
Start-Process 'docker' -NoNewWindow -ArgumentList "rm drbhandler"
Start-Process 'docker' -NoNewWindow -ArgumentList "rm drbconeremover"
Start-Process 'docker' -NoNewWindow -ArgumentList "rm drbwotupdater"
Start-Process 'docker' -NoNewWindow -ArgumentList "rm drbflasksite"