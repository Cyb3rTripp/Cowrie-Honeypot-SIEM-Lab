import json
import time
from datetime import datetime, timezone
from collections import defaultdict
from elasticsearch import Elasticsearch
import urllib3
from pathlib import Path

urllib3.disable_warnings()

# ----------------------------
# CONFIG
# ----------------------------

LOG_FILE = "/home/analyst/cowrie-analysis/logs/cowrie/cowrie.json"

CONFIG_FILE = Path(__file__).parent / "config.json"

with open(CONFIG_FILE) as f:
    config = json.load(f)

es = Elasticsearch(
    config["elastic_url"],
    basic_auth=(
        config["elastic_username"],
        config["elastic_password"]
    ),
    verify_certs=False
)

# ----------------------------
# STATE
# ----------------------------

seen = set()

sessions = defaultdict(lambda: {
    "ip": None,
    "commands": [],
    "categories": set(),
    "risk_score": 0
})

# ----------------------------
# RULES
# ----------------------------

CATEGORIES = {
    "RECON": ["whoami", "id", "uname", "ip a", "ifconfig", "netstat", "ps", "pwd"],
    "PRIVESC": ["sudo", "su", "chmod", "chown"],
    "DOWNLOAD": ["wget", "curl", "scp", "ftp"],
    "PERSISTENCE": ["crontab", "systemctl", "authorized_keys", ".ssh"],
    "PRIVESC_RECON": ["find / -perm", "getcap", "linpeas"]
}

RISK_SCORES = {
    "RECON": 1,
    "DOWNLOAD": 3,
    "PRIVESC": 5,
    "PERSISTENCE": 5,
    "PRIVESC_RECON": 4
}

# ----------------------------
# HELPERS
# ----------------------------

def classify(cmd: str):
    cmd = cmd.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in cmd:
                return category
    return None


def severity(score: int):
    if score >= 10:
        return "CRITICAL"
    elif score >= 6:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    return "LOW"


def emit(event: dict):
    try:
        es.index(index="cowrie-alerts", document=event)
    except Exception as e:
        # only real operational visibility
        print("[ELASTIC ERROR]", repr(e))


# ----------------------------
# PROCESSOR
# ----------------------------

def process(event: dict):

    if event.get("eventid") != "cowrie.command.input":
        return

    session = event.get("session", "unknown")
    ip = event.get("src_ip", "unknown")
    command = event.get("input", "")
    timestamp = event.get("timestamp", "")

    key = (session, timestamp, command)
    if key in seen:
        return
    seen.add(key)

    category = classify(command)

    sessions[session]["ip"] = ip
    sessions[session]["commands"].append(command)

    if category:
        sessions[session]["categories"].add(category)
        sessions[session]["risk_score"] += RISK_SCORES.get(category, 0)

    score = sessions[session]["risk_score"]
    level = severity(score)

    event_doc = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "session": session,
        "src_ip": ip,
        "command": command,
        "category": category or "UNKNOWN",
        "risk_score": score,
        "severity": level
    }

    emit(event_doc)


# ----------------------------
# SNAPSHOT LOOP
# ----------------------------

def run():
    while True:
        try:
            with open(LOG_FILE, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        process(event)
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print("[PIPELINE ERROR]", repr(e))

        time.sleep(2)


if __name__ == "__main__":
    run()
