#!bin/sh
echo "Stopping service"
systemctl stop HoneyGainWorker.service
echo "Disabling service"
systemctl disable HoneyGainWorker.service
echo "Removing service"
rm -rf /var/gvg/HoneyGainWorker.service
echo "Removing bash file"
rm -rf /var/gvg/RunHoneyGainWorker.sh
echo "Removing python request script"
rm -rf /var/gvg/request.py
#echo "Removing docker"
#apt-get -y remove docker.io
#apt-get -y remove docker-ce docker-ce-cli containerd.io
echo "Done"

