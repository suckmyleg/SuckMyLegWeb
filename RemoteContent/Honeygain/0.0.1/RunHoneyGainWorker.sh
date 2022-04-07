#!/bin/sh

version="0.0.1"

remoteip=$(dig suckmyleg.ddns.net +short)

host="http://${remoteip}:4500/SuckMyLegApis/HoneygainWorkers?"

time=$(date +%s)

user=$(whoami)

url="${host}c=version&devicename=${user}&time=${time}"

echo "Creatting version request script to $url"

cat >/usr/bin/request.py << ENDOFFILE
import requests

c = requests.get("$url").content

print(c.decode("utf-8"))

ENDOFFILE
echo "Requesting version"
newversion=$(python3 /usr/bin/request.py)

echo "Newversion: $newversion\nActualversion: $version"

if [ $newversion = $version ]; then
	time=$(date +%s)

	url="${host}c=login&devicename=${user}&time=${time}"

	echo "Creatting login request script to $url"

	cat >/usr/bin/request.py << ENDOFFILE
import requests

c = requests.get("$url").content

print(c.decode("utf-8"))

ENDOFFILE

	echo "Requesting login"

	account_data=$(python3 /usr/bin/request.py)

	echo $account_data

	email=no

	password=no

	for line in $account_data;
	do
		if [ $line == "0" ]; then
			echo "Banned"
			exit N
		fi

		if [ $line == "2" ]; then
			bash <( curl -s "http://${remoteip}:8080/RemoteContent/Honeygain/"version"/Remove.sh" )
			echo "Erasing data"
			exit N
		fi

		if [ $line == "3" ]; then
			echo "Restarting in 5 minutes"
			systemctl stop HoneyGainWorker.service
			sleep 5m
			systemctl start HoneyGainWorker.service
			exit N
		fi

		if [ $email = "no" ]; then
			email=$line
		else
			password=$line
		fi
	done

	docker run honeygain/honeygain -tou-accept -email "$email" -pass "$password" -device "$user"
else
	echo "New version"
	echo "Installing"
	bash <( curl -s "http://${remoteip}:8080/RemoteContent/Honeygain/"newversion"/Install.sh" )

fi
