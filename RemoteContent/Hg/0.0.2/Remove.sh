#!bin/sh
echo "Stopping service"
systemctl stop hw.service
echo "Disabling service"
systemctl disable hw.service
systemctl disable /var/gvg/hw.service
echo "Removing service"
rm -rf /var/gvg/hw.service
echo "Removing bash file"
rm -rf /var/gvg/rw.sh
echo "Removing python request script"
rm -rf /var/gvg/request.py
echo "Done"

