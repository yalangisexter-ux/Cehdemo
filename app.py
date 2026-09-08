from flask import Flask, jsonify, request
import sys
import os

# Add the current directory to the path so generate_project.py can be imported
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from generate_project import ProjectGenerator

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Android Project Generator API is running"
    })


# FIX: Allow both GET and POST so you can test in the browser
@app.route("/generate", methods=["GET", "POST"])
def generate_project():
    try:
        generator = ProjectGenerator()
        output_dir = generator.generate()

        return jsonify({
            "status": "success",
            "message": "Project generated successfully",
            "output_dir": output_dir
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
