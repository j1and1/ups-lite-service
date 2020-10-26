#!/usr/bin/env python3

import os

serviceContent = """[Unit]
Description=UPS lite service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 {0}/ups_service.py > /dev/null

[Install]
WantedBy=multi-user.target
""".format(os.getcwd())

with open('/lib/systemd/system/ups_lite.service', 'w') as out:
    out.write(serviceContent + '\n')

os.system('sudo chmod 644 /lib/systemd/system/ups_lite.service')