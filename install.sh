#/bin/bash
echo "Installing dependencies."
sudo apt update
sudo apt install python3 python3-pip python3-smbus i2c-tools -y
echo "Adding as service"
chmod +x ups_service.py
chmod +x service_installer.py
chmod +x uninstall.sh

sudo ./service_installer.py
sudo systemctl daemon-reload
sudo systemctl enable ups_lite.service
echo "Should be done now."