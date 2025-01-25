# SIEM Implementation & Log Analysis

## ⚠️ Disclaimer
This project is intended for educational and security research purposes only. Ensure you have the proper authorization before deploying a SIEM in any environment.

## Project Overview
- **Technology Used:** ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, Graylog
- **Purpose:** Deploy a Security Information and Event Management (SIEM) system to collect, analyze, and visualize security logs.
- **Output:** A functioning SIEM setup that centralizes logs and detects security incidents.

## Prerequisites
- Basic understanding of networking, security logs, and Linux
- A dedicated system or virtual machine for SIEM deployment
- Administrative access to configure log sources

## Setup and Implementation
### Step 1: Choose a SIEM Solution
- **ELK Stack:** Open-source log management and visualization system.
- **Splunk:** Enterprise-level SIEM with advanced analytics.
- **Graylog:** Open-source log management with built-in security features.

### Step 2: Install and Configure the SIEM
#### 1. Install ELK Stack (Example: Ubuntu/Debian)
```sh
sudo apt update && sudo apt install elasticsearch logstash kibana -y
```
#### 2. Install Splunk (Example: Download & Install)
```sh
wget -O splunk.deb https://download.splunk.com/products/splunk/releases/latest/linux/splunk-latest-linux-2.6-amd64.deb
sudo dpkg -i splunk.deb
```
#### 3. Install Graylog
```sh
sudo apt update && sudo apt install graylog-server -y
```

### Step 3: Configure Log Collection
- Set up **Logstash** to collect logs from various sources (firewalls, IDS, system logs).
- Configure **Splunk forwarders** for centralized log collection.
- Integrate **Graylog inputs** for network and system log ingestion.

#### Example Logstash Configuration for Syslog
```sh
input {
  udp {
    port => 514
    type => "syslog"
  }
}
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "syslog-%{+YYYY.MM.dd}"
  }
}
```

### Step 4: Enable Logging and Alerting
- Configure **SIEM dashboards** for log visualization.
- Set up **alerting rules** for suspicious activities.
- Define **log retention policies** for compliance.

#### Example Splunk Search for Failed SSH Logins
```sh
index=main sourcetype=linux_secure "Failed password" | stats count by user, host
```

### Step 5: Validate and Test SIEM Detection
- Generate test logs using `logger` in Linux.
```sh
logger "Test login failure"
```
- Use **nmap** to simulate network scans and review logs.
```sh
nmap -sS -p 22,80,443 192.168.1.10
```
- Check ELK Stack and Splunk dashboards for alerts.

## Key Features
- **Centralized log management**
- **Real-time security monitoring and alerting**
- **Customizable dashboards for log visualization**
- **Integration with IDS and firewalls for enhanced detection**

## Future Enhancements
- Automate incident response with SOAR (Security Orchestration, Automation, and Response)
- Integrate with **Threat Intelligence Feeds**
- Implement **Machine Learning for Anomaly Detection**

## Conclusion
A SIEM system enhances security visibility by centralizing logs and providing real-time monitoring. Using ELK Stack, Splunk, or Graylog ensures efficient log analysis, aiding in incident response and compliance.

## References
- [ELK Stack Documentation](https://www.elastic.co/what-is/elk-stack)
- [Splunk Docs](https://docs.splunk.com/Documentation)
- [Graylog Documentation](https://docs.graylog.org/en/latest/)
