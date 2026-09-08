import os
import sys
import json
import zipfile
import io
import base64
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================
PROJECT_NAME = "StealthApp_Advanced"
OUTPUT_DIR = "./generated_projects"
RENDER_DIR = "./render_files" # Directory where app.py and generate_project.py will be written

# ==============================================================================
# CORE GENERATION LOGIC (Simulating advanced_build functionality)
# ==============================================================================

def generate_android_project_logic():
    """
    Generates the Android project structure and returns it as a ZIP file in memory.
    This is the core logic that was previously embedded in the Flask app.
    
    Returns:
        tuple: (io.BytesIO object, filename)
    """
    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 1. Main Application Code
        main_code = f'''
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to {PROJECT_NAME}"

@app.route('/api/info')
def info():
    return jsonify({{"status": "active", "project": "{PROJECT_NAME}"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
        zip_file.writestr(f"{PROJECT_NAME}/main.py", main_code)
        
        # 2. Requirements
        requirements = "flask\ngunicorn\n"
        zip_file.writestr(f"{PROJECT_NAME}/requirements.txt", requirements)
        
        # 3. README
        readme = f'''# {PROJECT_NAME}

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`
'''
        zip_file.writestr(f"{PROJECT_NAME}/README.md", readme)
        
        # 4. Android-like structure (if applicable)
        android_dir = f"{PROJECT_NAME}/android"
        zip_file.writestr(f"{android_dir}/build.gradle", "# Android Build Config\n")
        zip_file.writestr(f"{android_dir}/AndroidManifest.xml", "<!-- Android Manifest -->\n")

    # Reset buffer to beginning
    zip_buffer.seek(0)
    
    return zip_buffer, f"{PROJECT_NAME}.zip"


# ==============================================================================
# FILE GENERATION FUNCTIONS
# ==============================================================================

def write_file(filepath, content):
    """Writes content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_app_py():
    """Generates the main app.py file that serves the UI and handles downloads."""
    
    # HTML Template for the Web Interface
    html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name }} Generator</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background-color: #121212; 
            color: #e0e0e0; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0;
        }
        .container { 
            text-align: center; 
            background: #1e1e1e; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.5); 
        }
        h1 { color: #007bff; margin-bottom: 20px; }
        p { margin-bottom: 30px; color: #b0b0b0; }
        button { 
            background-color: #007bff; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            font-size: 16px; 
            border-radius: 6px; 
            cursor: pointer; 
            transition: background 0.3s;
        }
        button:hover { background-color: #0056b3; }
        #status { 
            margin-top: 20px; 
            font-weight: bold; 
            min-height: 24px; 
        }
        .success { color: #28a745; }
        .error { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ project_name }} Generator</h1>
        <p>Click below to generate and download your advanced project ZIP.</p>
        <button onclick="generateProject()">Generate & Download</button>
        <div id="status"></div>
    </div>

    <script>
        async function generateProject() {
            const statusEl = document.getElementById('status');
            statusEl.className = '';
            statusEl.innerText = "Generating...";
            
            try {
                // Send POST request to the generate endpoint
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({}) // Empty body, logic is server-side
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "{{ project_name }}.zip";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    
                    statusEl.innerText = "Download started!";
                    statusEl.className = 'success';
                } else {
                    statusEl.innerText = "Error: " + response.statusText;
                    statusEl.className = 'error';
                }
            } catch (error) {
                statusEl.innerText = "Network Error: " + error.message;
                statusEl.className = 'error';
            }
        }
    </script>
</body>
</html>
'''

    app_py_content = f'''
import os
import io
import zipfile
from flask import Flask, render_template_string, request, send_file, jsonify
from generate_project import generate_android_project_logic

app = Flask(__name__)

# Embedded HTML Template
HTML_TEMPLATE = {repr(html_template)}

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template_string(
        HTML_TEMPLATE, 
        project_name="{PROJECT_NAME}"
    )

@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate the Android project and return it as a ZIP file.
    This is triggered by the frontend button, not by a direct URL visit.
    """
    try:
        zip_data, filename = generate_android_project_logic()
        
        return send_file(
            zip_data,
            mimetype='application/zip',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500

@app.route('/health')
def health():
    return jsonify({{"status": "ok"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
    return app_py_content

def generate_generate_project_py():
    """Generates generate_project.py which contains the core logic."""
    
    generate_project_content = f'''
import io
import zipfile
from datetime import datetime

def generate_android_project_logic():
    """
    Generates the Android project structure and returns it as a ZIP file in memory.
    
    Returns:
        tuple: (io.BytesIO object, filename)
    """
    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 1. Main Application Code
        main_code = f'''
from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to {PROJECT_NAME}"

@app.route('/api/info')
def info():
    return jsonify({{"status": "active", "project": "{PROJECT_NAME}"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''
        zip_file.writestr(f"{PROJECT_NAME}/main.py", main_code)
        
        # 2. Requirements
        requirements = "flask\ngunicorn\n"
        zip_file.writestr(f"{PROJECT_NAME}/requirements.txt", requirements)
        
        # 3. README
        readme = f'''# {PROJECT_NAME}

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python main.py`
'''
        zip_file.writestr(f"{PROJECT_NAME}/README.md", readme)
        
        # 4. Android-like structure (if applicable)
        android_dir = f"{PROJECT_NAME}/android"
        zip_file.writestr(f"{android_dir}/build.gradle", "# Android Build Config\\n")
        zip_file.writestr(f"{android_dir}/AndroidManifest.xml", "<!-- Android Manifest -->\\n")

    # Reset buffer to beginning
    zip_buffer.seek(0)
    
    return zip_buffer, f"{PROJECT_NAME}.zip"
'''
    return generate_project_content

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print(f"Generating advanced build files for {PROJECT_NAME}...")
    
    # 1. Generate app.py
    app_content = generate_app_py()
    write_file(os.path.join(RENDER_DIR, "app.py"), app_content)
    print(f"✅ Created: {RENDER_DIR}/app.py")
    
    # 2. Generate generate_project.py
    generate_project_content = generate_generate_project_py()
    write_file(os.path.join(RENDER_DIR, "generate_project.py"), generate_project_content)
    print(f"✅ Created: {RENDER_DIR}/generate_project.py")
    
    # 3. Generate requirements.txt for Render
    requirements_content = "flask\ngunicorn\n"
    write_file(os.path.join(RENDER_DIR, "requirements.txt"), requirements_content)
    print(f"✅ Created: {RENDER_DIR}/requirements.txt")
    
    print(f"\n🚀 Deployment Instructions:")
    print(f"1. Upload {RENDER_DIR}/app.py, {RENDER_DIR}/generate_project.py, and {RENDER_DIR}/requirements.txt to your Render repository.")
    print(f"2. Set Build Command: `pip install -r requirements.txt`")
    print(f"3. Set Start Command: `gunicorn app:app`")
    print(f"4. Deploy!")

if __name__ == "__main__":
    main()
