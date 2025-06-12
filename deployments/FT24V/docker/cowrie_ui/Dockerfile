FROM cowrie/cowrie
COPY ./cowrie.cfg /cowrie/cowrie-git/etc/cowrie.cfg
COPY ./userdb.txt /cowrie/cowrie-git/etc/userdb.txt
COPY ./etc/banner.txt /cowrie/cowrie-git/share/banner.txt
COPY ./etc/passwd /cowrie/cowrie-git/honeyfs/etc/passwd
COPY ./etc/shadow /cowrie/cowrie-git/honeyfs/etc/shadow
COPY ./etc/group /cowrie/cowrie-git/honeyfs/etc/group
COPY ./etc/cmdoutput.json /cowrie/cowrie-git/src/cowrie/data/cmdoutput.json
COPY ./commands/netstat.py /cowrie/cowrie-git/cowrie/commands/netstat.py