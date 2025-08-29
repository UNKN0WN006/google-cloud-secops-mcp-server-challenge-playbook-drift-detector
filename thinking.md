# Thought Process & Journey: Building the MCP Playbook Drift Detector

## 1. **Initial Idea**

The challenge was to showcase the Google SecOps MCP server in a creative, practical way. I wanted to build something that:
- Demonstrates real-world security automation,
- Is visually impressive,
- Is easy for others to run and understand.

I decided on a **drift detector** for playbooks, since configuration drift is a real pain point in security operations.

---

## 2. **First Steps & Early Failures**

- **Started with a simple Flask server** to serve a static playbook.
- Tried to fetch the playbook with a Python script, but kept getting connection errors.
    - Realized I forgot to start the server before running the script!
- Added more endpoints, but hit CORS issues when testing with browser tools.
    - Switched to using only Python clients for simplicity.

---

## 3. **Expanding the Scope**

- Added more playbooks to the server to make it feel realistic.
- Tried to compare playbooks using plain string comparison, but it was hard to see what changed.
    - Switched to using `difflib` for unified diffs, which made drift detection much clearer.

---

## 4. **Making It Human-Friendly**

- Wanted a dashboard, so I embedded Flask in the detector too.
- First dashboard attempt was ugly and hard to use.
    - Iterated on the HTML/CSS until it looked clean and simple.
- Added a "Re-run" button so users could check for drift without restarting the app.

---

## 5. **Handling Errors and Edge Cases**

- Sometimes the server would crash if a playbook name was missing.
    - Added error handling for missing playbooks and network failures.
- Accidentally overwrote baseline files a few times.
    - Added checks to only save a baseline if it didn't exist.

---

## 6. **Simulating Real-World Use**

- Added a drift simulation thread to the server so I could demo drift detection live.
- Created multiple playbooks that mimic real security workflows (phishing, IAM, WAF, etc.).
- Made sure the dashboard could handle any number of playbooks.

---

## 7. **Final Polish**

- Added audit logs and alert endpoints to the server for realism.
- Made sure all code was modular and variable names were short but clear.
- Wrote a README and took screenshots for the submission.

---

## 8. **Lessons Learned**

- Always start the server before running the client!
- Handle every possible error—real users will hit them.
- Visual feedback (dashboard, diffs) makes demos much more compelling.
- Iteration is key: every failure taught me something and improved the project.

---

## 9. **How a Human Would Run This**

1. Start the mock server:
    ```sh
    python3 mock_server.py
    ```
2. In a new terminal, start the detector/dashboard:
    ```sh
    python3 playbook_detector.py
    ```
3. Open the dashboard:
    ```sh
    $BROWSER http://localhost:5050/
    ```
4. Change a playbook via the server or API, then re-run drift detection to see it in action.

---