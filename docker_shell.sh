#!/bin/bash

#-v $(pwd):/app -w /app
docker run \
    -v $(pwd)/python:/root/python \
    -w /app \
    --rm \
    -w /root/python \
    -it \
    billybag2/mestastic-mqtt:latest /bin/bash 