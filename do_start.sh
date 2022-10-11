#!/bin/bash

# This is applicable to dev only
if [ -d "./misc" ]; then
  (
    cd ./misc ;
    bash freeze_requirements.sh ;
  )
fi

docker compose build ;
docker compose up ;
docker compose down ;
