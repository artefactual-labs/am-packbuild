#!/bin/sh -eux

# Restart dashboard on failure (helps on boot)
sed -i 's/User=archivematica/Restart=on-failure\nRestartSec=30\nUser=archivematica/g' /etc/systemd/system/archivematica-dashboard.service
