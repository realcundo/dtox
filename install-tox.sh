#!/bin/bash
set -e -u -x

echo "tox version: $TOX_VERSION"

# install pip and other packages
apt-get update
apt-get install -y python-pip rsync
rm -rf /var/lib/apt/lists/*

# install tox
pip install tox==$TOX_VERSION

# set up test user
useradd testuser -ms /bin/bash

# to be continued...
