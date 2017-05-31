#!/bin/bash

mkdir -p mmdb || exit 1
cd mmdb || exit 1
rm -rf *
wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz || exit 1
tar -zxvf GeoLite2-Country*.tar.gz || exit 1
cd GeoLite2-Country* || exit 1
sudo mkdir -p /opt/mmdb/database/ || exit 1
sudo cp -v GeoLite2-Country.mmdb /opt/mmdb/database/ || exit 1
sudo cp -v GeoLite2-Country.mmdb ../../../SOURCES/ || exit 1
