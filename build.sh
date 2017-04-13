#!/bin/bash
sudo docker build --rm -t opi2051-002:5000/cls-blweb:latest . ; sudo docker push opi2051-002:5000/cls-blweb:latest
#docker rmi $(docker images -q -f "dangling=true")
