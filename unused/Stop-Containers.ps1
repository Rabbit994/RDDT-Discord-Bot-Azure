Start-Process 'docker' -NoNewWindow -ArgumentList "stop drblistener"
Start-Process 'docker' -NoNewWindow -ArgumentList "stop drbhandler"
Start-Process 'docker' -NoNewWindow -ArgumentList "stop drbconeremover"
Start-Process 'docker' -NoNewWindow -ArgumentList "stop drbwotupdater"
Start-Process 'docker' -NoNewWindow -ArgumentList "stop drbflasksite"
Start-Sleep 15 #Let the Docker Containers finishing stopping