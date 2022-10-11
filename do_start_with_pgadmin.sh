#!/bin/bash

# This is applicable to dev only
if [ -d "./misc" ]; then
  (
    cd ./misc ;
    bash freeze_requirements.sh ;
  )
fi

docker_compose="docker compose -f docker-compose.yml -f docker-compose.pgadmin.yml"

$docker_compose build ;
$docker_compose up ;
$docker_compose down ;
