# Intrusion Detection System (IDS) Deployment

## ⚠️ Disclaimer
This project is intended for educational and security research purposes only. Ensure you have the proper authorization before deploying an IDS in any environment.

## Project Overview
- **Technology Used:** Snort, Suricata, Zeek (Bro), Security Onion
- **Purpose:** Deploy an Intrusion Detection System (IDS) to monitor and detect malicious activities on a network.
- **Output:** A functioning IDS setup that can log and alert on suspicious network traffic.

## Prerequisites
- Basic understanding of networking and security concepts
- A dedicated system or virtual machine for IDS deployment
- Administrative access to configure network interfaces

## Setup and Implementation
### Step 1: Choose an IDS Solution
- **Snort:** Open-source network-based IDS (NIDS) with strong community support.
- **Suricata:** Multi-threaded IDS with high-performance capabilities.
- **Zeek (Bro):** Focuses on network traffic analysis beyond signatures.

### Step 2: Install and Configure the IDS
#### 1. Install Snort (Example: Ubuntu/Debian)
```sh
sudo apt update && sudo apt install snort -y
```
#### 2. Install Suricata (Example: Ubuntu/Debian)
```sh
sudo apt update && sudo apt install suricata -y
```
#### 3. Configure Snort to Monitor Network Traffic
- Edit the Snort configuration file: `/etc/snort/snort.conf`
- Define network variables (e.g., HOME_NET, EXTERNAL_NET)
- Enable appropriate rule sets

```sh
var HOME_NET [192.168.1.0/24]
var EXTERNAL_NET any
```

#### 4. Configure Suricata to Monitor Network Traffic
- Edit the Suricata configuration file: `/etc/suricata/suricata.yaml`
- Define network variables and logging options
- Enable IDS mode

```yaml
vars:
  address-groups:
    HOME_NET: "[192.168.1.0/24]"
    EXTERNAL_NET: "any"
```

#### 5. Test Snort and Suricata Configuration
```sh
sudo snort -T -c /etc/snort/snort.conf
sudo suricata -T -c /etc/suricata/suricata.yaml
```

### Step 3: Enable Logging and Alerting
- Configure Snort to log alerts to `/var/log/snort/alert`
- Configure Suricata to log alerts to `/var/log/suricata/fast.log`
- Set up an alerting mechanism (e.g., Syslog, Email, SIEM integration)

#### Example Snort Rule to Detect Ping Scans
```sh
alert icmp any any -> $HOME_NET any (msg:"ICMP Ping Detected"; sid:1000001; rev:1;)
```

#### Example Suricata Rule for SSH Brute Force Detection
```yaml
alert tcp any any -> $HOME_NET 22 (msg:"Potential SSH Brute Force"; threshold:type both, track by_src, count 5, seconds 60; sid:2000001; rev:1;)
```

### Step 4: Deploy IDS in a Network Environment
- Place the IDS on a **SPAN/mirror port** or **network TAP** for optimal monitoring.
- Ensure proper firewall rules allow IDS traffic analysis.

### Step 5: Validate and Test IDS Detection
- Use tools like **nmap** to simulate attacks.
```sh
nmap -sS -p 22,80,443 192.168.1.10
```
- Check Snort logs for detected events.
```sh
cat /var/log/snort/alert
```
- Check Suricata logs for detected events.
```sh
cat /var/log/suricata/fast.log
```

## Key Features
- **Real-time network traffic analysis**
- **Customizable rule-based detection**
- **Multi-threaded processing with Suricata for high performance**
- **Seamless integration with SIEM solutions**

## Future Enhancements
- Implement threat intelligence feeds for improved detection.
- Integrate with a Security Information and Event Management (SIEM) system.
- Automate incident response with Python-based scripts.

## Conclusion
Deploying an IDS enhances network security by detecting malicious activities in real-time. Using both Snort and Suricata provides a robust detection framework, leveraging signature-based and advanced protocol analysis techniques. Regular updates to IDS rules and integration with SIEM improve overall security posture.

## References
- [Snort Official Documentation](https://www.snort.org/documents)
- [Suricata Documentation](https://suricata.io/documentation/)
- [Zeek (Bro) Guide](https://docs.zeek.org/en/stable/)

