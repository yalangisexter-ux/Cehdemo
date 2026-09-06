package com.example.securitylab

import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

object UpdateInstaller {
    fun downloadAndInstall(context: Context, apkUrl: String, fileName: String) {
        Thread {
            try {
                val url = URL(apkUrl)
                val connection = (url.openConnection() as HttpURLConnection).apply {
                    requestMethod = "GET"
                    connectTimeout = 15000
                    readTimeout = 15000
                }

                val file = File(context.cacheDir, fileName)
                connection.inputStream.use { input ->
                    file.outputStream().use { output ->
                        input.copyTo(output)
                    }
                }
                connection.disconnect()

                val packageInstaller = context.packageManager.packageInstaller
                val params = PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL)
                val sessionId = packageInstaller.createSession(params)
                val session = packageInstaller.openSession(sessionId)

                session.openWrite("package_session", 0, file.length()).use { output ->
                    file.inputStream().use { input ->
                        input.copyTo(output)
                    }
                    output.fsync()
                }

                val intent = Intent(context, InstallReceiver::class.java).apply {
                    action = "com.example.securitylab.ACTION_INSTALL_COMPLETE"
                }
                val pendingIntent = PendingIntent.getBroadcast(
                    context,
                    sessionId,
                    intent,
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
                )

                session.commit(pendingIntent.intentSender)
                session.close()

            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }
}
