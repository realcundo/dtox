FROM ubuntu:trusty

MAINTAINER github.com/realcundo

ENV TOX_VERSION 2.3.1
ENV PYTHON_VERSIONS "2.3 2.4 2.5 2.6 2.7 3.2 3.3 3.4 3.5"
ENV GOSU_VERSION 1.9

ENTRYPOINT /bin/bash

COPY install-pythons.sh install-gosu.sh /

RUN /bin/bash /install-pythons.sh \
 && /bin/bash /install-gosu.sh \
 && rm /install-*.sh

# temporarily separate tox install to speed up builds
COPY install-tox.sh /
RUN /bin/bash /install-tox.sh \
 && rm /install-*.sh
