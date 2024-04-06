#!/bin/bash

command="mosquitto_sub -h ${DEFAULT_HOST} -t ${WILDCARD_TOPIC} -u ${DEFAULT_USER} -P ${DEFAULT_PASS}"
echo "Running command: ${command}"
$command
