#!/bin/sh -eux

# Restart archivematica-storage-service on failure (helps on boot)
sed -i 's/User=archivematica/Restart=on-failure\nRestartSec=10\nUser=archivematica/g' /etc/systemd/system/archivematica-storage-service.service

