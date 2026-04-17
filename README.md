# Automated Website Monitoring & Self-Healing System

A Python-based infrastructure monitoring system that continuously checks application health, sends alerts on failure, and automatically attempts recovery using server-level and container-level remediation.

---

## Features

* Monitors application uptime every 5 minutes
* Sends email alerts when the service is down
* Automatically restarts failed Docker containers via SSH
* Reboots Linode instance if container-level recovery fails
* Fully automated incident response workflow with minimal manual intervention

---

## Tech Stack

* Python
* Requests (HTTP monitoring)
* Paramiko (SSH automation)
* Linode API (infrastructure management)
* SMTP (email alerting)
* Schedule (task scheduling)

---

## How It Works

1. The script runs every 5 minutes using a scheduler
2. It checks the target web application health endpoint
3. If the service is healthy (HTTP 200), it does nothing
4. If the service is unhealthy:

   * Sends an email alert
   * Attempts to restart the Docker container via SSH
   * If recovery fails, triggers a Linode server reboot
5. Once the server is back online, services are restarted automatically

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env` file

```env
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
LINODE_TOKEN=your_linode_api_token
SSH_KEY_PATH=path_to_your_private_key
```

---

## Run the script

```bash
python monitor-website.py
```

---

## Purpose

This project demonstrates:

* Basic site reliability engineering (SRE) principles
* Automated incident detection and recovery
* Cloud infrastructure control using APIs
* Remote server management via SSH

It is designed as a lightweight self-healing system for small deployments or personal projects.
