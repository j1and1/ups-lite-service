#/bin/bash
echo "Uninstalling dependencies."

sudo systemctl stop ups_lite.service
sudo systemctl disable ups_lite.service
sudo rm /lib/systemd/system/ups_lite.service
sudo systemctl daemon-reload

echo "Done"