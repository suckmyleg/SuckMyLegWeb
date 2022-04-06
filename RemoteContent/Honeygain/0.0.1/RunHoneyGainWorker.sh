#!/bin/sh

version="0.0.1"

host="http://localhost:4500/SuckMyLegApis/HoneygainWorkers?"

time="%s"

user=$(whoami)

cat >/usr/bin/request.py << ENDOFFILE
import requests

print(requests.get("${host}command=version&devicename=${user}&time=${time}&ip=${ip}").content)

ENDOFFILE

newversion=$(python3 request.py)

if [ $newversion = $version ]; then
	time="%s"

	cat >/usr/bin/request.py << ENDOFFILE
	import requests

	print(requests.get("${host}command=login&devicename=${user}&time=${time}&ip=${ip}").content)

ENDOFFILE

	account_data=$(python3 request.py)

	email=no

	password=no

	for line in $account_data;
	do
		if [ $line == "0" ]; then
			echo "Banned"
			exit N
		fi

		if [ $line == "2" ]; then
			bash <( curl -s "http://localhost:8080/RemoteContent/Honeygain/"version"/Remove.sh" )
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

	bash <( curl -s "http://localhost:8080/RemoteContent/Honeygain/"newversion"/Install.sh" )

fi
