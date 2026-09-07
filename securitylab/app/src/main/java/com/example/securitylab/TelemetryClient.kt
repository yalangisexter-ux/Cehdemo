package com.example.securitylab

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
