# Image for haproxy
FROM ubuntu:21.10

RUN set -ex \
    && export DEBIAN_FRONTEND=noninteractive \
    && echo 'APT::Install-Recommends "0";\nAPT::Install-Suggests "0";' > /etc/apt/apt.conf.d/01norecommend \
    && apt-get update -y \
    && apt-get install -y haproxy python3-pip plocate iproute2  \
               dnsutils iputils-ping sudo psmisc --fix-missing \
    && pip3 install jinja2 \
    && mkdir -p /data \
    && updatedb

COPY templates/* /data/templates/
COPY entrypoint.py /

ENTRYPOINT ["/usr/bin/python3", "/entrypoint.py"]
