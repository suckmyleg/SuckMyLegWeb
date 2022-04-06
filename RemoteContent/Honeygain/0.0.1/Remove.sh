#!bin/sh
echo "Stopping service"
systemctl stop HoneyGainWorker.service
echo "Disabling service"
systemctl disable HoneyGainWorker.service
echo "Removing service"
rm -rf /usr/bin/HoneyGainWorker.service
echo "Removing bash file"
rm -rf /usr/bin/RunHoneyGainWorker.sh
echo "Removing python request script"
rm -rf /usr/bin/request.py
#echo "Removing docker"
#apt-get -y remove docker.io
#apt-get -y remove docker-ce docker-ce-cli containerd.io
echo "Done"

