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


