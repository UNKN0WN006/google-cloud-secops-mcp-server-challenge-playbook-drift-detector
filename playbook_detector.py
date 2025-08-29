import requests
import difflib
import os
from datetime import datetime
from flask import Flask, render_template_string, send_file, jsonify

SRV = "http://localhost:8086"
PBS = ["default", "advanced", "phishing_investigation", "cloud_storage_audit", "iam_anomaly_detection", "web_app_firewall_monitor"]
B_DIR = "baselines"
D_DIR = "drift_reports"
ALRT = f"{SRV}/api/alerts"
PORT = 5050

def ensure_dirs():
    os.makedirs(B_DIR, exist_ok=True)
    os.makedirs(D_DIR, exist_ok=True)

def b_path(pb): return os.path.join(B_DIR, f"{pb}.yaml")
def d_path(pb): return os.path.join(D_DIR, f"drift_{pb}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt")

def fetch(pb):
    try:
        r = requests.get(f"{SRV}/api/playbooks/{pb}")
        return r.text if r.status_code == 200 else None
    except Exception:
        return None

def load_b(pb):
    p = b_path(pb)
    return open(p).read() if os.path.exists(p) else None

def save_b(pb, c):
    with open(b_path(pb), "w") as f: f.write(c)

def diff_b(b, c):
    return list(difflib.unified_diff(b.splitlines(keepends=True), c.splitlines(keepends=True), fromfile="baseline", tofile="current"))

def alert(pb, diff):
    data = {"timestamp": datetime.utcnow().isoformat(), "type": "playbook_drift", "playbook": pb, "details": "".join(diff)}
    try: requests.post(ALRT, json=data)
    except Exception: pass

class R:
    def __init__(self, pb, drift, dfile=None): self.pb, self.drift, self.dfile = pb, drift, dfile

def check(pb):
    c = fetch(pb)
    if c is None: return R(pb, False)
    b = load_b(pb)
    if b is None:
        save_b(pb, c)
        return R(pb, False)
    if b == c: return R(pb, False)
    diff = diff_b(b, c)
    dp = d_path(pb)
    with open(dp, "w") as f: f.writelines(diff)
    alert(pb, diff)
    return R(pb, True, dp)

def run_all():
    ensure_dirs()
    return [check(pb) for pb in PBS]

tmpl = """
<!DOCTYPE html><html><head><title>MCP Drift</title>
<style>body{font-family:sans-serif;}th,td{padding:8px;}th{background:#eee;}</style>
</head><body>
<h2>MCP Playbook Drift Dashboard</h2>
<table border=1><tr><th>Playbook</th><th>Status</th><th>Drift Report</th></tr>
{% for r in res %}
<tr>
<td>{{r.pb}}</td>
<td>{% if r.drift %}<b style="color:#c00">Drift</b>{% else %}<span style="color:#080">OK</span>{% endif %}</td>
<td>{% if r.drift %}<a href="/drift/{{r.pb}}">View</a>{% else %}-{% endif %}</td>
</tr>
{% endfor %}
</table>
<form method="POST" action="/rerun"><button type="submit">Re-run</button></form>
</body></html>
"""

def dash_app():
    app = Flask(__name__)
    app.config['res'] = run_all()

    @app.route('/')
    def dash(): return render_template_string(tmpl, res=app.config['res'])

    @app.route('/drift/<pb>')
    def drift(pb):
        files = [f for f in os.listdir(D_DIR) if f.startswith(f"drift_{pb}_")]
        if not files: return "No drift report.", 404
        latest = sorted(files)[-1]
        return send_file(os.path.join(D_DIR, latest), mimetype="text/plain")

    @app.route('/rerun', methods=['POST'])
    def rerun():
        app.config['res'] = run_all()
        return dash()

    @app.route('/api/status')
    def api_status():
        return jsonify([{"pb": r.pb, "drift": r.drift, "dfile": r.dfile} for r in app.config['res']])

    return app

def main():
    ensure_dirs()
    print(f"[INFO] Dashboard: http://localhost:{PORT}/")
    dash_app().run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    main()