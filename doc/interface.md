# Local Interface Installation Guide

This guide describes the steps to install and configure the local interface for the honeynet deployment.

---

## 1. Configure iptables Rules

Set the default policies and add the following rules to control the traffic:

```bash
# Set default policies
-P INPUT DENY
-P FORWARD ACCEPT
-P OUTPUT ACCEPT

# Allow established connections
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

# Allow loopback interface
-A INPUT -i lo -j ACCEPT

# Allow new TCP connections on custom SSH port
-A INPUT -p tcp -m tcp --dport <custom_ssh_port> -m state --state NEW -j ACCEPT

# Allow traffic on wlan0
-A INPUT -i wlan0 -j ACCEPT
```

---

## 2. Configure Wi-Fi

Create or edit the `wpa_supplicant.conf` file with the following content:

```ini
country=us
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
    scan_ssid=1
    ssid="<your_wifi_ssid>"
    psk="<your_wifi_password>"
}
```

For more information, see the [Raspberry Pi Spy article](https://www.raspberrypi-spy.co.uk/2017/04/manually-setting-up-pi-wifi-using-wpa_supplicant-conf/).

---

## 3. Hide SSH

Change the SSH port to your custom port and restart the SSH service:

```bash
sudo sh -c 'echo "Port <custom_ssh_port>" >> /etc/ssh/sshd_config'
sudo /etc/init.d/ssh restart
```

---

## 4. Enable IP Routing

Enable IP forwarding by appending the following line to `/etc/sysctl.conf`:

```bash
sudo sh -c 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf'
```

---

## 5. Configure IP Addresses

Configure the IP addresses for your interfaces. For persistent configuration, append the commands to `/etc/rc.local`.

### For `wlan0`:

```bash
sudo sh -c 'sudo ip a add <ip_address_1> dev wlan0 >> /etc/rc.local'
sudo sh -c 'sudo ip a add <ip_address_2> dev wlan0 >> /etc/rc.local'
sudo sh -c 'sudo ip a add <ip_address_3> dev wlan0 >> /etc/rc.local'
sudo sh -c 'sudo ip a add <ip_address_4> dev wlan0 >> /etc/rc.local'
```

### For `eth0`:

```bash
sudo sh -c 'sudo ip a add <ip_address_5> dev eth0'
sudo sh -c 'sudo ip a add <ip_address_6> dev eth0'
sudo sh -c 'sudo ip a add <ip_address_7> dev eth0'
sudo sh -c 'sudo ip a add <ip_address_8> dev eth0'
sudo sh -c 'sudo ip a add <ip_address_9> dev eth0'
```

Create a symbolic link for the honeynet script:

```bash
sudo ln -s ../init.d/honeynet S99honeynet
```

---

## 6. Install WireGuard and Dependencies

Install WireGuard and other required packages:

```bash
sudo apt-get install wireguard -y
sudo apt install openresolv -y
sudo apt install iptables -y
```

---

## 7. Configure WireGuard

### 7.1 Generate WireGuard Keys

Generate the private and public keys:

```bash
sudo wg genkey | sudo tee /etc/wireguard/private.key | sudo wg pubkey | sudo tee /etc/wireguard/public.key
```

### 7.2 Configure WireGuard Interface: `wg0.conf`

Create a file named `wg0.conf` with the following content:

```ini
[Interface]
Address = <wg0_address>
DNS = 8.8.8.8
PostUp = wg set %i private-key /etc/wireguard/private.key
PostUp = ping -c1 <internal_ping_address>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_1> -j DNAT --to-destination <destination_ip_1>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_2> -j DNAT --to-destination <destination_ip_2>

[Peer]
PublicKey = <peer_public_key_1>
AllowedIPs = <allowed_ips_1>
Endpoint = <wg0_endpoint>
```

### 7.3 Configure WireGuard Interface: `wg1.conf`

Create a file named `wg1.conf` with the following content:

```ini
[Interface]
Address = <wg1_address>
DNS = 8.8.8.8
PostUp = wg set %i private-key /etc/wireguard/private.key
PostUp = ping -c1 <internal_ping_address>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_1> -j DNAT --to-destination <destination_ip_3>
PostUp = sudo iptables -t nat -A PREROUTING -d <ip_address_2> -j DNAT --to-destination <destination_ip_4>

[Peer]
PublicKey = <peer_public_key_2>
AllowedIPs = <allowed_ips_2>
Endpoint = <wg1_endpoint>
```

Enable the WireGuard interface:

```bash
sudo systemctl enable wg-quick@wg0
```

---

## 8. Enable Logging for Suspicious Packets

Insert the following iptables rules to log suspicious packets:

```bash
sudo iptables -I FORWARD 1 -j LOG --log-level info --log-prefix "***SUSPICIOUS PACKET: "
sudo iptables -I INPUT 1 -j LOG --log-level info --log-prefix "***SUSPICIOUS PACKET: "
```

