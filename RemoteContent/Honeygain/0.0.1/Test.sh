#!/bin/sh

read -p "Transmit installer? y/n" answer

ifconfig

read -p "Network to expand" network_ip

if [ $answer = 'y' ]; then

	echo "Searching devices on network"

	output=$(nmap -sn $network_ip/24)

	for line in $output; 
	do
		if [[ "Nmap scan report for" = *$line* ]]; then
			echo $line
		fi
	done 

fi