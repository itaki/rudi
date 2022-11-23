#!/bin/sh

# inspiration : https://gist.github.com/grant-roy/49b2c19fa88dcffc46ab


cd ..
cd rudi-app

git fetch
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

echo $LOCAL
echo $REMOTE