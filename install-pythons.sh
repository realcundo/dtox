#!/bin/bash
set -e -u -x

# construct package names from versions (python$VER-dev)
PYTHON_PACKAGES=`sed 's/[0-9.]\+/python\0-dev/g' <<< "$PYTHON_VERSIONS"`

echo "python versions: $PYTHON_VERSIONS ($PYTHON_PACKAGES)"

# get fkrull and pypy keys
export GNUPGHOME="$(mktemp -d)"

gpg --keyserver keyserver.ubuntu.com --recv-keys DB82666C
gpg --export DB82666C | apt-key add -

gpg --keyserver keyserver.ubuntu.com --recv-keys 68854915
gpg --export 68854915 | apt-key add -

# new repos for historical pythons and pypy
echo deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main >> /etc/apt/sources.list
echo deb-src http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu trusty main >> /etc/apt/sources.list

echo deb http://ppa.launchpad.net/pypy/ppa/ubuntu trusty main >> /etc/apt/sources.list
echo deb-src http://ppa.launchpad.net/pypy/ppa/ubuntu trusty main >> /etc/apt/sources.list

# update and install pythons and pypy
apt-get update
apt-get install -y \
    $PYTHON_PACKAGES \
    pypy-dev

# remove gpg stuff
rm -r "$GNUPGHOME"

# remove downloaded package files
# use apt-get update to re-download them
rm -rf /var/lib/apt/lists/*
