package com.example.securitylab

import android.content.Context
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

object InstallationLogger {
    private const val LOG_DIR = "install_logs"
    private const val LOG_FILE = "installation.log"

    fun logEvent(context: Context, eventType: String, details: String) {
        try {
            val logDir = File(context.cacheDir, LOG_DIR)
            if (!logDir.exists()) {
                logDir.mkdirs()
            }

            val logFile = File(logDir, LOG_FILE)
            val timestamp = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US).format(Date())
            val logEntry = "[$timestamp] $eventType: $details\n"

            logFile.appendText(logEntry)
        } catch (e: Exception) {
            // Silent failure - don't propagate
        }
    }

    fun clearLogs(context: Context) {
        try {
            val logDir = File(context.cacheDir, LOG_DIR)
            if (logDir.exists()) {
                logDir.deleteRecursively()
            }
        } catch (e: Exception) {
            // Silent failure
        }
    }

    fun getLogs(context: Context): String {
        return try {
            val logFile = File(context.cacheDir, "$LOG_DIR/$LOG_FILE")
            if (logFile.exists()) logFile.readText() else "No logs available"
        } catch (e: Exception) {
            "Error reading logs"
        }
    }
}
