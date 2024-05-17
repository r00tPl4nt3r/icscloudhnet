FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    strongswan \
    xl2tpd \
    ppp \
    iptables

COPY ./etc/ipsec.conf /etc/ipsec.conf
COPY ./etc/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf
COPY ./etc/ppp/options.l2tpd.client /etc/ppp/options.l2tpd.client

CMD ["sh", "-c", "ipsec start --nofork && xl2tpd"]