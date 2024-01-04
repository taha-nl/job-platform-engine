#!/bin/bash
%sh
LAST_VERSION="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2FLAST_CHANGE?alt=media"
VERSION=$(curl -s -S $LAST_VERSION)
if [ -d $VERSION ] ; then
  echo "version already installed"
  exit
fi
 
rm -rf /tmp/chrome/$VERSION
mkdir -p /tmp/chrome/$VERSION
 
URL="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F$VERSION%2Fchrome-linux.zip?alt=media"
ZIP="${VERSION}-chrome-linux.zip"
 
curl -# $URL > /tmp/chrome/$ZIP
unzip /tmp/chrome/$ZIP -d /tmp/chrome/$VERSION
 
URL="https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F$VERSION%2Fchromedriver_linux64.zip?alt=media"
ZIP="${VERSION}-chromedriver_linux64.zip"
 
curl -# $URL > /tmp/chrome/$ZIP
unzip /tmp/chrome/$ZIP -d /tmp/chrome/$VERSION
 
mkdir -p /tmp/chrome/chrome-user-data-dir
 
rm -f /tmp/chrome/latest
ln -s /tmp/chrome/$VERSION /tmp/chrome/latest
 
# to avoid errors about missing libraries
# sudo apt-get update
# sudo apt-get install -y libgbm-dev
apt-get update
apt-get install -y libgbm-dev
