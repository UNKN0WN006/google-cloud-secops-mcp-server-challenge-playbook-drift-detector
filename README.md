# Automated Playbook Drift Detection & Remediation with SecOps MCP Server

## Overview

This project leverages the SecOps MCP server to automatically detect when a security automation playbook drifts from the approved baseline. By continuously monitoring for changes, it ensures your security automations remain current and effective, reducing manual review and minimizing the risk of outdated responses.

---

## How It Works

1. **Fetches** the current playbook from the MCP server.
2. **Compares** it with the baseline version stored locally.
3. **Alerts** the team if any difference (drift) is detected and generates a detailed report.

---

## Impact

- **Before:** Manual, infrequent playbook reviews led to outdated automations and missed incidents.
- **After:** Automated drift detection keeps playbooks aligned and response sharp.

---

## Usage Instructions

1. Place your baseline playbook as `baseline_playbook.yaml` in the same folder.
2. Update the `MCP_SERVER_URL` variable in the script to your MCP server endpoint.
3. Run the script:
   ```sh
   python3 playbook_drift_detector.py
   ```
4. Review the output and the generated drift report for alerts.

---

## Screenshot

---

## License

This project is provided for educational purposes only and nothing more to expect from it.
