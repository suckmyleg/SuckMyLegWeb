#!/bin/sh

version="0.0.1"

dir="/var/gvg/"

remoteip=$(dig sw22.ddns.net +short)

host="http://${remoteip}:8443/Apis/HoneygainWorkers?"

time=$(date +%s)

user=$(whoami)

url="${host}c=version&devicename=${user}&time=${time}"

echo "Creatting version request script to $url"

cat > ${dir}request.py << ENDOFFILE
import requests

c = requests.get("$url").content

print(c.decode("utf-8"))

ENDOFFILE
echo "Requesting version"
newversion=$(python3 ${dir}request.py)

echo "Newversion: $newversion\nActualversion: $version"

if [ $newversion = $version ]; then
	time=$(date +%s)

	url="${host}c=login&devicename=${user}&time=${time}"

	echo "Creatting login request script to $url"

	cat > ${dir}request.py << ENDOFFILE
import requests

c = requests.get("$url").content

print(c.decode("utf-8"))

ENDOFFILE

	echo "Requesting login"

	account_data=$(python3 ${dir}request.py)

	echo $account_data

	email=no

	password=no

	IFS=' '

	read -ra lines <<< "$account_data"

	for line in "${lines[@]}";
	do
		if [ $line == "0" ]; then
			echo "Banned"
			exit N
		fi

		if [ $line == "2" ]; then
			echo "Erasing data"
			bash <( curl -s "http://${remoteip}:8080/RemoteContent/Hg/"${version}"/Remove.sh" )
			exit N
		fi

		if [ $line == "3" ]; then
			echo "Restarting in 5 minutes"
			systemctl stop hw.service
			sleep 5m
			systemctl start hw.service
			exit N
		fi

		if [ $email = "no" ]; then
			email=$line
		else
			password=$line
		fi
	done

	nohup docker run honeygain/honeygain -tou-accept -email "$email" -pass "$password" -device "$user" &

	url="${host}c=alive&devicename=${user}&time=${time}"

	cat > ${dir}request.py << ENDOFFILE
import requests

c = requests.get("$url").content

print(c)
ENDOFFILE

	while :
	do
		t=$(python3 ${dir}request.py)s
		sleep $t
	done
else
	echo "New version"
	echo "Installing"
	bash <( curl -s "http://${remoteip}:8080/RemoteContent/Hg/"${newversion}"/Install.sh" )

fi
