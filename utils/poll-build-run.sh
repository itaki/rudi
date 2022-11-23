#!/bin/bash
# inspiration : https://gist.github.com/grant-roy/49b2c19fa88dcffc46ab

# Usage: From the repo root, run "sh utils/poll-build-run.sh" (if you run it from within th utils folder it won't work right)
# Note: In order to continuously check for updates, docker compose runs in detached mode (i.e. runs the container in the background). If you want to debug live on the pi you should stop the polling script and run docker-compose in normal mode (without the -d param)


cd rudi-app

echo "Polling for changes..."
while true
do


git fetch
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})


if [ $LOCAL != $REMOTE ]; then

    echo "Change detected!"
    echo "Updating local files with the latest from Github"!
    git pull
    echo "Stopping any containers that might be running"
    docker compose down --remove-orphans
    echo "Deleting any and all previous containers"
    docker system prune -f
    echo "Building and running a brand new container"
    docker compose up --build -d
    echo "Polling for changes..."

fi
sleep 5
done
