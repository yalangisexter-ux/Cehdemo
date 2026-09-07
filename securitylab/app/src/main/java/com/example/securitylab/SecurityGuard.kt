package com.example.securitylab

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
