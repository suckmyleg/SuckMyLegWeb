#!/bin/sh

version="0.0.1"

host="http://localhost:4500/SuckMyLegApis/HoneygainWorkers?"

time="%s"

user=$(whoami)

newversion=$(wget $host"command=version&devicename=${user}&time=${time}&ip=${ip}" -q -O -)

if [ $newversion = $version ]; then
	time="%s"

	account_data=$(wget $host"command=login&devicename=${user}&time=${time}&ip=${ip}" -q -O -)

	email=no

	password=no

	for line in $account_data:
		if [ $line = 0 ]; then
			echo "Banned"
			exit N
		fi

		if [ $line = 2 ]; then
			bash <( curl -s "http://localhost:8080/RemoteContent/Honeygain/"version"/Remove.sh" )
			echo "Erasing data"
			exit N
		fi

		if [ $line = 3 ]; then
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

	docker run honeygain/honeygain -tou-accept -email "$email" -pass "$password" -device "$user"
else

	bash <( curl -s "http://localhost:8080/RemoteContent/Honeygain/"newversion"/Install.sh" )

fi
