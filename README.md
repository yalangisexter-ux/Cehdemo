# CEH Demo Lab - Server & Android Project

Comprehensive Android security education platform with Flask backend and complete Android project generator.

## Components

### Flask Server (app.py)
- **Endpoint**: `/collect` (POST)
- **Purpose**: Receives and logs data exfiltrated from Android devices
- **Output**: `collected_data.txt` with timestamped entries

### Android Project Generator (generate_project.py)
Run locally to generate complete Android CEH Lab workspace:
```bash
python3 generate_project.py
```

Generates `android-ceh-lab.zip` containing:

#### **Attacker Module** (`com.cehlab.attacker`)
- SMS/Call interception and manipulation
- Location tracking (GPS)
- Audio recording via microphone
- Contact & call log extraction
- Data exfiltration to server
- Auto-start on device boot
- Notification listener service

#### **Defender Module** (`com.cehlab.defender`)
- Advanced system auditor
- Permission analysis
- Detects dangerous permission combinations
- Identifies malicious accessibility/notification listener abuse
- Overlay + spyware combo detection

#### **Root Audit Module** (`com.cehlab.rootaudit`)
- Device root status detection
- Checks for su binaries
- Magisk framework detection
- Build tag analysis

## Setup & Deployment

### Local Development
```bash
pip install -r requirements.txt
python app.py
```

### Render Deployment
- Push to connected Render service
- Server runs on port 5000 (configurable via PORT env var)
- Data collected in `collected_data.txt`
- Live at: `https://cehdemo.onrender.com`

## Usage

1. Deploy server to Render
2. Generate Android project: `python3 generate_project.py`
3. Open in Android Studio, build & deploy attacker APK
4. Run on test device, grant permissions
5. Activate "System Service" to start data collection
6. Monitor collected data in server logs
7. Use Defender app to detect and analyze threats
8. Use Root Audit to verify device integrity

## Security Note
⚠️ **Educational Purpose Only** - This lab demonstrates Android security vulnerabilities for learning. Unauthorized access to devices or data is illegal.
