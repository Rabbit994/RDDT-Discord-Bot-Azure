Start-Process 'docker' -ArgumentList "stop drblistener"
Start-Process 'docker' -ArgumentList "stop drbhandler"
Start-Process 'docker' -ArgumentList "stop drbconeremover"
Start-Process 'docker' -ArgumentList "stop drbwotupdater"
Start-Process 'docker' -ArgumentList "stop drbflasksite"
Start-Sleep 15 #Let the Docker Containers finishing stopping