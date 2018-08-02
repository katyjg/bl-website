#!/bin/bash
sudo docker build --rm -t srv-cmcf-dp4:5000/cls-blweb:latest . && sudo docker push srv-cmcf-dp4:5000/cls-blweb:latest
sudo docker rmi $( sudo docker images -q -f "dangling=true")

