from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/playbooks', methods=['GET'])
def get_playbook():
    # A sample playbook as plain text or JSON
    playbook = """
steps:
  - name: check_login_attempts
    action: query_logs
    params:
      source: auth
      threshold: 5
  - name: notify_team
    action: send_alert
    params:
      channel: security
"""
    return playbook, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)