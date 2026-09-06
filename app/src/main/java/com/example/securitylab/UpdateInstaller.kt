package com.example.securitylab

import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import kotlin.math.min

object UpdateInstaller {
    private const val BUFFER_SIZE = 8192
    private const val CONNECT_TIMEOUT = 15000
    private const val READ_TIMEOUT = 15000
    private const val SESSION_NAME = "package_session"
    private const val ACTION_INSTALL_COMPLETE = "com.example.securitylab.ACTION_INSTALL_COMPLETE"

    fun downloadAndInstall(
        context: Context,
        apkUrl: String,
        fileName: String,
        onProgress: ((downloaded: Long, total: Long) -> Unit)? = null,
        onComplete: ((success: Boolean, message: String) -> Unit)? = null
    ) {
        Thread {
            try {
                // Download APK
                val file = downloadApk(apkUrl, context, fileName, onProgress)
                if (file == null) {
                    onComplete?.invoke(false, "Download failed")
                    return@Thread
                }

                // Install APK
                val success = installApk(context, file, fileName)
                onComplete?.invoke(success, if (success) "Installation initiated" else "Installation failed")

            } catch (e: Exception) {
                onComplete?.invoke(false, "Error: ${e.message}")
            }
        }.apply { name = "UpdateInstaller-Thread" }.start()
    }

    private fun downloadApk(
        apkUrl: String,
        context: Context,
        fileName: String,
        onProgress: ((downloaded: Long, total: Long) -> Unit)? = null
    ): File? {
        return try {
            val url = URL(apkUrl)
            val connection = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = "GET"
                connectTimeout = CONNECT_TIMEOUT
                readTimeout = READ_TIMEOUT
                doInput = true
            }

            if (connection.responseCode != HttpURLConnection.HTTP_OK) {
                return null
            }

            val totalSize = connection.contentLength
            val file = File(context.cacheDir, fileName)

            connection.inputStream.use { input ->
                file.outputStream().use { output ->
                    val buffer = ByteArray(BUFFER_SIZE)
                    var bytesRead: Int
                    var totalDownloaded = 0L

                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                        totalDownloaded += bytesRead
                        onProgress?.invoke(totalDownloaded, totalSize.toLong())
                    }
                }
            }
            connection.disconnect()
            file
        } catch (e: Exception) {
            null
        }
    }

    private fun installApk(context: Context, apkFile: File, fileName: String): Boolean {
        return try {
            val packageInstaller = context.packageManager.packageInstaller
            val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL)
            val sessionId = packageInstaller.createSession(params)
            val session = packageInstaller.openSession(sessionId)

            // Write APK to session
            session.openWrite(SESSION_NAME, 0, apkFile.length()).use { output ->
                apkFile.inputStream().use { input ->
                    val buffer = ByteArray(BUFFER_SIZE)
                    var bytesRead: Int
                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                    }
                    output.fsync()
                }
            }

            // Create install intent
            val intent = Intent(context, InstallReceiver::class.java).apply {
                action = ACTION_INSTALL_COMPLETE
                putExtra("sessionId", sessionId)
            }
            val pendingIntent = PendingIntent.getBroadcast(
                context,
                sessionId,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            // Commit installation
            session.commit(pendingIntent.intentSender)
            session.close()
            true
        } catch (e: Exception) {
            false
        }
    }
}
