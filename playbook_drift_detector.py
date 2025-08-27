import requests
import difflib
import os
import sys
from datetime import datetime

MCP_SERVER_URL = "http://localhost:5000/api/playbooks"
BASELINE_PATH = "baseline_playbook.yaml"
ALERT_LOG = "drift_alerts.log"
DRIFT_REPORT = "drift_report.txt"

def get_current_playbook():
    try:
        response = requests.get(MCP_SERVER_URL, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        return ""

def get_baseline_playbook():
    if not os.path.exists(BASELINE_PATH):
        return ""
    with open(BASELINE_PATH, "r") as f:
        return f.read()

def write_drift_report(diff_lines):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DRIFT_REPORT, "w") as report:
        report.write(f"Drift Report - {now}\n\n")
        for line in diff_lines:
            report.write(line)
    return DRIFT_REPORT

def log_alert(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ALERT_LOG, "a") as log:
        log.write(f"[{now}] {message}\n")

def alert_team(report_path):
    print("ALERT: Playbook drift detected!")
    print(f"See detailed drift report: {report_path}")
    log_alert(f"Drift detected. Report: {report_path}")

def update_baseline(new_content):
    with open(BASELINE_PATH, "w") as f:
        f.write(new_content)

def main():
    print("Checking for playbook drift...")
    current_playbook = get_current_playbook()
    baseline_playbook = get_baseline_playbook()
    if not current_playbook:
        print("Could not fetch current playbook from MCP server.")
        sys.exit(1)
    if not baseline_playbook:
        print("Baseline playbook not found. Creating new baseline.")
        update_baseline(current_playbook)
        print("Baseline created.")
        sys.exit(0)
    if current_playbook == baseline_playbook:
        print("No drift detected. Playbook is up to date.")
        sys.exit(0)
    current_lines = current_playbook.splitlines(keepends=True)
    baseline_lines = baseline_playbook.splitlines(keepends=True)
    diff = list(difflib.unified_diff(baseline_lines, current_lines, fromfile="baseline_playbook.yaml", tofile="current_playbook.yaml"))
    if diff:
        report_path = write_drift_report(diff)
        alert_team(report_path)
        print("Drift details:")
        for line in diff:
            print(line, end="")
    else:
        print("No significant drift detected.")

if __name__ == "__main__":
    main()
    