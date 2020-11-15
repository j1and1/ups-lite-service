# Raspberry pi UPS Lite as a service

This was made inspiring by [linshuqin329/UPS-Lite](https://github.com/linshuqin329/UPS-Lite) readout implementation.

This service has will shutdown your Raspberry Pi when the battery reaches `20%` while discharging if the pi is not plugged in. Before shutdown it will send a notification using `wall` to let you know pi is going to shutdown

## Install process

This is easy to setup as you will just need to clone this repo and run `install.sh` to install the service and `uninstall.sh` to uninstall the service.

If you haven't installed git then you should run before install
```
sudo apt update
sudo apt install git
```

after git has been installed run
```
git clone https://github.com/j1and1/ups-lite-service.git
cd ups-lite-service
chmod +x install.sh
./install.sh
```

You can check if the install is successful by running `sudo systemctl status ups_lite.service` if install was successful the output of that command should look like this
```
pi@raspberrypi:~ $ sudo systemctl status ups_lite.service
● ups_lite.service - UPS lite service
   Loaded: loaded (/lib/systemd/system/ups_lite.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2020-11-15 10:33:16 GMT; 2s ago
 Main PID: 20711 (python3)
    Tasks: 1 (limit: 995)
   CGroup: /system.slice/ups_lite.service
           └─20711 /usr/bin/python3 /home/pi/ups-lite-service/ups_service.py > /dev/null

Nov 15 10:33:16 raspberrypi systemd[1]: Started UPS lite service.
```

# TODOs

- [ ] Make the shutdown procentage configurable
- [ ] Add more warnings before shutdown
- [ ] Code cleanup