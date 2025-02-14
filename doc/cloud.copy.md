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

## 2. Clone Repository and Run 
See details in [Deployments](/deployments/README.md)

```bash
git clone clone https://github.com/r00tPl4nt3r/trapnet
cd <repository_name>/
sudo sh install.sh
cd deployments/<deployment_path>/docker/
sudo docker compose up -d
```

---

## 3. Hide SSH

Change SSH port to enhance security:

```bash
sudo sh -c 'echo "Port <custom_ssh_port>" >> /etc/ssh/sshd_config'
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
sudo sh -c 'sudo ip a add <ip_address_1> dev docker0'
sudo sh -c 'sudo ip a add <ip_address_2> dev docker0'
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
Address = <vpn_address>/32 
ListenPort = <vpn_port>
PrivateKey = <your_private_key>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_1> -p tcp --dport 22 -j REDIRECT --to-ports <ssh_port_1>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_2> -p tcp --dport 22 -j REDIRECT --to-ports <ssh_port_2>

[Peer]
PublicKey = <peer_public_key>
AllowedIPs = <vpn_client_ip>/32, <network_1>/24, <network_2>/24
```

Replace `<your_private_key>`, `<peer_public_key>`, `<ip_address_1>`, `<ip_address_2>`, `<vpn_address>`, `<vpn_port>`, `<vpn_client_ip>`, `<network_1>`, `<network_2>`, `<ssh_port_1>`, and `<ssh_port_2>` with the appropriate values.

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

