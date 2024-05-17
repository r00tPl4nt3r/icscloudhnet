FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    strongswan \
    xl2tpd \
    ppp \
    iptables

COPY ./ipsec.conf /etc/ipsec.conf
COPY ./xl2tpd.conf /etc/xl2tpd/xl2tpd.conf
COPY ./options.xl2tpd /etc/ppp/options.xl2tpd
COPY ./chap-secrets /etc/ppp/chap-secrets

CMD ["sh", "-c", "ipsec start --nofork && xl2tpd"]