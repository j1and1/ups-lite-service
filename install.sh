#/bin/bash
echo "Installing dependencies."
sudo apt install python3 python3-pip python3-smbus i2c-tools libnotify-bin -y
echo "Adding as service"