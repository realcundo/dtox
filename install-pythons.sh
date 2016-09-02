#!/bin/bash
set -e -u

# construct package names from versions (python$VER-dev)
PYTHON_PACKAGES=`sed 's/[0-9.]\+/python\0-dev/g' <<< "$PYTHON_VERSIONS"`

echo "python versions: $PYTHON_VERSIONS ($PYTHON_PACKAGES)"

# get fkrull and pypy keys
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
    curl \
	$PYTHON_PACKAGES \
    pypy-dev \
	python-pip

rm -rf /var/lib/apt/lists/*
