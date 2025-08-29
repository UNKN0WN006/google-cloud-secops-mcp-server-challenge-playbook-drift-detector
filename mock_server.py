from flask import Flask, request, jsonify, render_template_string
import datetime
import threading

app = Flask(__name__)

# Playbook storage (in-memory)
playbooks = {
    "default": """steps:
  - name: check_login_attempts
    action: query_logs
    params:
      source: auth
      threshold: 5
  - name: notify_team
    action: send_alert
    params:
      channel: security
""",
    "advanced": """steps:
  - name: check_failed_logins
    action: query_logs
    params:
      source: auth
      threshold: 10
  - name: escalate
    action: send_alert
    params:
      channel: secops
  - name: block_user
    action: block_account
    params:
      user_field: username
""",
    "phishing_investigation": """steps:
  - name: extract_urls
    action: parse_email
    params:
      field: body
  - name: check_url_reputation
    action: query_threat_intel
    params:
      source: VirusTotal
  - name: quarantine_email
    action: quarantine
    params:
      mailbox: user
""",
    "cloud_storage_audit": """steps:
  - name: list_buckets
    action: gcp_list_buckets
    params: {}
  - name: check_public_access
    action: gcp_check_acl
    params:
      access: public
  - name: alert_on_public
    action: send_alert
    params:
      channel: cloudsec
""",
    "iam_anomaly_detection": """steps:
  - name: list_iam_changes
    action: gcp_list_iam_changes
    params:
      timeframe: 24h
  - name: detect_unusual_roles
    action: analyze_roles
    params:
      threshold: 2
  - name: escalate
    action: send_alert
    params:
      channel: identity
""",
    "web_app_firewall_monitor": """steps:
  - name: fetch_waf_logs
    action: query_logs
    params:
      source: waf
      timeframe: 1h
  - name: detect_sql_injection
    action: pattern_match
    params:
      pattern: sql_injection
  - name: block_ip
    action: block_ip
    params:
      duration: 3600
"""
}
audit_log = []
alerts = []

def log_action(action, details):
    audit_log.append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action": action,
        "details": details
    })

@app.route('/')
def index():
 # Dashboard
    dashboard = """
    <h2>MCP Mock Server Dashboard</h2>
    <ul>
      <li><a href='/api/playbooks/default'>View Default Playbook</a></li>
      <li><a href='/api/playbooks/advanced'>View Advanced Playbook</a></li>
      <li><a href='/api/audit'>View Audit Log</a></li>
      <li><a href='/api/alerts'>View Alerts</a></li>
    </ul>
    """
    return render_template_string(dashboard)

@app.route('/api/playbooks/<name>', methods=['GET'])
def get_playbook(name):
    pb = playbooks.get(name)
    log_action("get_playbook", {"name": name})
    if pb:
        return pb, 200, {'Content-Type': 'text/plain'}
    return "Not found", 404

@app.route('/api/playbooks/<name>', methods=['POST'])
def update_playbook(name):
    content = request.data.decode('utf-8')
    playbooks[name] = content
    log_action("update_playbook", {"name": name, "content": content})
    return "Updated", 200

@app.route('/api/playbooks', methods=['GET'])
def list_playbooks():
    log_action("list_playbooks", {})
    return jsonify(list(playbooks.keys()))

@app.route('/api/audit', methods=['GET'])
def get_audit():
    return jsonify(audit_log)

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts)

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    alert = request.json
    alerts.append(alert)
    log_action("create_alert", alert)
    return jsonify({"status": "alert received"}), 201

# Periodic drifting
def simulate_drift():
    import time
    while True:
        time.sleep(120)  # Each and every 2 minutes
        playbooks["default"] = playbooks["default"].replace("threshold: 5", "threshold: 7")
        log_action("simulate_drift", {"name": "default", "change": "threshold: 5 -> threshold: 7"})

if __name__ == '__main__':
    drift_thread = threading.Thread(target=simulate_drift, daemon=True)
    drift_thread.start()
    app.run(host='0.0.0.0', port=8086)