from flask import Flask, request, jsonify

app = Flask(__name__)
current_command = "harvest"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "Security Lab Server is Running"}), 200

@app.route('/command', methods=['GET'])
def get_command():
    global current_command
    return current_command, 200

@app.route('/command', methods=['POST'])
def set_command():
    global current_command
    data = request.get_json() or {}
    current_command = data.get('command', 'harvest')
    return jsonify({"status": "success", "command": current_command}), 200

@app.route('/telemetry', methods=['POST'])
def receive_telemetry():
    data = request.get_json() or {}
    print(f"Received telemetry payload: {data}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)