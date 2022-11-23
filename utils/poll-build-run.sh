#!/bin/sh
# inspiration : https://gist.github.com/grant-roy/49b2c19fa88dcffc46ab

# Usage: From the repo root, run "sh utils/poll-build-run.sh"
# Note: In order to continuously check for updates, docker compose runs in detached mode (i.e. runs the container in the background). If you want to debug live on the pi you should stop the polling script and run docker-compose in normal mode (without the -d param)


# make sure this script runs properly regardless of qwhere the user is when they call it
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

#move into the app folder
cd ..
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
    echo "Stopping any running Docker containers"
    docker compose down --remove-orphans
    echo "Building and running new container"
    docker compose up --build -d

fi
sleep 5
done