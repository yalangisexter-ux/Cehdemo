from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/collect', methods=['POST'])
def collect():
    data = request.get_json()
    print(f"[{datetime.datetime.now()}] Received: {data}")
    with open("collected_data.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} {data}\n")
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))