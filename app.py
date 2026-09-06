import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "lab": "CEH Security Education Lab Backend",
        "endpoints": ["/collect", "/health"]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/collect', methods=['POST'])
def collect_data():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or request.data.decode('utf-8', errors='ignore')
        print(f"[Lab Data Received]: {data}")
        return jsonify({
            "status": "success",
            "message": "Data successfully exfiltrated/recorded",
            "received": data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
