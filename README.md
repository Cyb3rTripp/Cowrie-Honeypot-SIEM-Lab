# Cowrie Honeypot SIEM Lab
A self-hosted cybersecurity lab that captures attacker activity using the Cowrie SSH honeypot, analyzes attacker behavior with a custom Python detection pipeline, and visualizes security events in Elasticsearch and Kibana.

This project demonstrates the design and implementation of a small-scale Security Operations Center (SOC) monitoring pipeline:

**Attacker → Cowrie Honeypot → Log Collection → Python Analysis Pipeline → Elasticsearch → Kibana Dashboard**

## Project Overview

The goal of this project was to build a complete honeypot monitoring and alerting pipeline from the ground up.

The environment consists of:

- A **Cowrie SSH honeypot server**
- A **Kali Linux attacker machine** used to generate simulated attacker activity
- An **Ubuntu analysis workstation**
- **Elasticsearch** for event storage and search
- **Kibana** for visualization and dashboarding
- A custom **Python ingestion and detection pipeline**
- A **systemd service** to automate log processing

The final system continuously monitors Cowrie logs, identifies attacker commands, categorizes activity, assigns risk scores, and forwards the resulting security events to Elasticsearch for analysis.

## Architecture
![Architecture Screenshot](https://github.com/Cyb3rTripp/Cowrie-Honeypot-SIEM-Lab/blob/main/Screenshots/Architecture.png)

## Key Features
- SSH honeypot deployment using Cowrie
- Simulated attacker activity from Kali Linux
- Automated Cowrie log collection
- Passwordless SSH authentication for automation
- Scheduled log synchronization using ```cron```
- Custom Python log ingestion pipeline
- Command classification based on attacker behavior
- Session-based risk scoring
- Severity assignment based on cumulative activity
- Elasticsearch event indexing
- Kibana data visualization
- Automated pipeline execution using ```systemd```
- SOC-style dashboards for security monitoring

## Lab Environment
### Honeypot Server
| Component | Configuration |
|-----------|---------------|
|Operating System |Ubuntu Server |
|CPU |2 Cores |
|Memory |4 GB RAM |
|Storage  | 20 GB |
|Honeypot | Cowrie |
|Primary Protocol | SSH |

### Analysis Workstation
| Component | Configuration |
|-----------|---------------|
|Operating System |Ubuntu Desktop |
|CPU |2 Cores |
|Memory |4 GB RAM |
|Storage  | 30 GB |
|SIEM Stack | Elasticsearch + Kibana |
|Analysis | Python |

### Attacker Machine
| Component | Purpose |
|-----------|---------------|
|Kali Linux |Simulated Attacker Activity |
|SSH Client |Connects to Cowrie |
|Command Execution |Generates Honeypot Telemetry |

## 1. Cowrie Honeypot Deployment

The first stage of the project was deploying Cowrie on an Ubuntu Server virtual machine.

Cowrie provides a controlled SSH environment designed to capture and record attacker interaction. Instead of exposing a real production system, the honeypot provides a monitored environment where attacker behavior can be safely observed.

The honeypot was configured with a realistic hostname to make the environment appear more authentic to an attacker.

### Example Connection

```ssh anything@<HONEYPOT_IP> -p 2222```

Once connected, commands entered by the simulated attacker are recorded in Cowrie's JSON log files.

### Example Attacker Activity

```
whoami 
pwd 
cat /etc/passwd 
uname -a
```

Cowrie records information including:

- Source IP address
- Session ID
- Timestamp
- Commands executed
- Authentication activity
- Connection information

**Simulated attacker activity interacting with the Cowrie SSH honeypot:**
![Attacker atcivity in Cowrie SSH honeypot](https://github.com/Cyb3rTripp/Cowrie-Honeypot-SIEM-Lab-Draft/blob/main/Screenshots/Attacker%20Honeypot%20Activity.png)

## 2. Automated Log Collection
