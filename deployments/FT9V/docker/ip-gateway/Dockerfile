FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    strongswan \
    xl2tpd \
    ppp \
    iptables

COPY ./etc/ /etc


CMD ["sh", "-c", "ipsec start --nofork && xl2tpd"]