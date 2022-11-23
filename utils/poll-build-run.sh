#!/bin/sh
# inspiration : https://gist.github.com/grant-roy/49b2c19fa88dcffc46ab

#if [ $# -lt 1 ]; then
#  echo 1>&2 "$0: missing branch parameter"
#  exit 2
#elif [ $# -gt 1 ]; then
#  echo 1>&2 "$0: too many parameters"
#  exit 2
#fi
#BRANCH=$1

cd ..
cd rudi-app

echo Polling for changes...

while true
do


git fetch #origin $BRANCH
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})


if [ $LOCAL != $REMOTE ]; then

    echo Change detected!
    git pull


fi
sleep 5
done