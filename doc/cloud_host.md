# Cloud/Fog Server Installation Guide

This guide provides the steps to install and configure the cloud or fog server for the honeynet deployment.

---

## 1. Install Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/raspbian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

---

## 2. Clone Repository and run deployment (go to deployments for detailed instructions.)

```bash
git clone https://github.com/r00tPl4nt3r/icscloudhnet
cd icscloudhnet/
sudo sh install.sh
cd deployments/FT9V/docker/
sudo docker compose up -d
```

---

## 3. Hide SSH

Change SSH port to enhance security:

```bash
sudo sh -c 'echo "Port 54344" >> /etc/ssh/sshd_config'
sudo /etc/init.d/ssh restart
```

---

## 4. Enable Routing

Enable IP forwarding:

```bash
sudo sh -c 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf'
```

---

## 5. Configure IP Addresses

Assign IP addresses to `docker0`:

```bash
sudo sh -c 'sudo ip a add 172.17.1.10 dev docker0'
sudo sh -c 'sudo ip a add 172.17.1.5 dev docker0'
```

Create a symbolic link for the honeynet startup:

```bash
sudo ln -s ../init.d/honeynet S99honeynet
```

---

## 6. Install WireGuard and Dependencies

```bash
sudo apt-get install wireguard -y
sudo apt install openresolv -y
sudo apt install iptables -y
```

---

## 7. Configure WireGuard

### 7.1 Generate WireGuard Keys

```bash
sudo wg genkey | sudo tee /etc/wireguard/private.key | sudo wg pubkey | sudo tee /etc/wireguard/public.key
```

### 7.2 Configure WireGuard Interface: `wg1.conf`

Create a file named `wg1.conf` with the following content:

```ini
[Interface]
Address = 10.20.20.1/32
ListenPort = 51149
PrivateKey = <your_private_key>
PostUp = sudo iptables -t nat -A PREROUTING -d 172.17.1.10 -p tcp --dport 22 -j REDIRECT --to-ports 2022
PostUp = sudo iptables -t nat -A PREROUTING -d 172.17.1.5 -p tcp --dport 22 -j REDIRECT --to-ports 2522

[Peer]
PublicKey = <peer_public_key>
AllowedIPs = 10.20.20.3/32, 192.168.0.0/24, 192.168.99.0/24
```

Replace `<your_private_key>` and `<peer_public_key>` with your actual keys.

---

## 8. Logging Modules

Enable packet logging with iptables:

```bash
sudo iptables -I FORWARD 1 -j LOG --log-level info --log-prefix "***SUSPICIOUS PACKET: "
sudo iptables -t nat -A INPUT -j LOG --log-level info --log-prefix "**SUSPICIOUS NAT: "
```

---

## 9. Log Collection

### 9.1 Monitor Kernel Logs

```bash
journalctl -k -f
```

### 9.2 Monitor Docker Logs

```bash
sudo docker ps -q | xargs -L 1 -P $(sudo docker ps | wc -l) sudo docker logs --since 30s -f
```

