#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /var/www/backend
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop portfolio-api
docker rm portfolio-api
docker rmi al7262/portfolio:backend
docker run -d --name portfolio-api -p 5000:5000 al7262/portfolio:latest