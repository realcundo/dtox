FROM ubuntu:trusty

ENV TOX_VERSION 2.3.1
ENV PYTHON_VERSIONS "2.3 2.4 2.5 2.6 2.7 3.2 3.3 3.4 3.5"

COPY install-pythons.sh /install-pythons.sh

RUN /bin/bash /install-pythons.sh \
 && rm /install-pythons.sh \
 && pip install tox==$TOX_VERSION

ENTRYPOINT /bin/bash
