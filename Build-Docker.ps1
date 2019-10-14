Start-Process 'docker' -NoNewWindow -ArgumentList "build --no-cache -f discord_listener.dockerfile . -t drblistener:latest" -Wait #let first build run to get python image downloaded
Start-Process 'docker' -NoNewWindow -ArgumentList "build --no-cache -f message_handler.dockerfile . -t drbhandler:latest" -Wait
Start-Process 'docker' -NoNewWindow -ArgumentList "build --no-cache -f cone_remover.dockerfile . -t drbconeremover:latest" -Wait
Start-Process 'docker' -NoNewWindow -ArgumentList "build --no-cache -f wot_updater.dockerfile . -t drbwotupdater:latest" -Wait
Start-Process 'docker' -NoNewWindow -ArgumentList "build --no-cache -f flask_site.dockerfile . -t drbflasksite:latest" -Wait