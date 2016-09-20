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

# /src is the RO input source
# /code is the main working dir which we can optionally
# symlink to
mkdir -p /src /code
chown testuser:testuser /src /code

# move custom tox to its place
chmod +x /tox.sh
mv /tox.sh `which tox`

# to be continued...
