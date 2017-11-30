#!/bin/bash
sudo docker build --rm -t opi2051-002:5000/cls-blweb:refresh . ; sudo docker push opi2051-002:5000/cls-blweb:refresh
#docker rmi $(docker images -q -f "dangling=true")
