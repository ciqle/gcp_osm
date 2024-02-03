#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: download_pbf.sh <PBF_DEST_PATH>"
  exit 1
fi

PBF_DEST_PATH=$1
mkdir -p $PBF_DEST_PATH
cd $PBF_DEST_PATH
axel -n 4 https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf

local_md5=$(md5sum planet-latest.osm.pbf | awk '{print $1}')
remote_md5=$(curl -s https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf.md5 | awk '{print $1}')

if [ "$local_md5" == "$remote_md5" ]; then
  echo "Local and remote MD5 checksums match, download succeeded."
else
  echo "Error: Local and remote MD5 checksums do not match"
fi