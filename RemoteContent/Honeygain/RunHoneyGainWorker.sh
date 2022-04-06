#!/bin/sh

host=http://www.suckmyleg.ddns.net:8080/SuckMyLegApis/HoneygainWorkers

data=$(wget  -q -O -)

docker run honeygain/honeygain -tou-accept -email "$mail" -pass "$pass" -device "$device"