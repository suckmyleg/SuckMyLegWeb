#!/bin/sh
version="0.0.4"
dir="/var/gvg/"
remoteip=192.168.1.104
user=$(whoami)
echo "Requesting version"
newversion=$(python3 ${dir}request.py "version" ${user})
echo "Newversion: $newversion\nActualversion: $version"
if [ "$newversion" == "$version" ]; then
	while :
	do
		echo "Requesting login"
		account_data=$(python3 ${dir}request.py "login" ${user})
		echo $account_data
		email=no
		password=no
		IFS=' '
		read -ra lines <<< "$account_data"
		i=0
		for line in "${lines[@]}";
		do
			if [ "$line" == "0" ]; then
				echo "Banned"
				exit N
			fi
			if [ "$line" == "2" ]; then
				echo "Erasing data"
				bash <( curl -s "http://${remoteip}:8080/RemoteContent/Hg/"${version}"/Remove.sh" )
				exit N
			fi
			if [ "$line" == "3" ]; then
				echo "Restarting in 5 minutes"
				systemctl stop hw.service
				sleep 5m
				systemctl start hw.service
				exit N
			fi
			if [ "$i" == 0 ]; then
				email=$line
			fi
			if [ "$i" == 1 ]; then
				password=$line
			fi
			i=$((i+1))
		done
		if [[ "$password" == "no" ]]; then
			echo "No password"
		else
			nohup docker run honeygain/honeygain -tou-accept -email "$email" -pass "$password" -device "$user" &
		fi
			while :
			do
				t=$(python3 ${dir}request.py "alive" ${user})s
				sleep $t
			done
	done
else
	echo "New version"
	echo "Installing"
	bash <( curl -s "http://${remoteip}:8080/RemoteContent/Hg/"${newversion}"/Install.sh" )
fi
