package com.example.securitylab

import android.util.Log
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object TelemetryClient {
    private const val ENDPOINT_URL = "https://cehdemo.onrender.com/collect"

    fun sendData(moduleName: String, telemetryData: String) {
        Thread {
            var connection: HttpURLConnection? = null
            try {
                val url = URL(ENDPOINT_URL)
                connection = (url.openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    setRequestProperty("Content-Type", "application/json; charset=utf-8")
                    setRequestProperty("Accept", "application/json")
                    doOutput = true
                    connectTimeout = 10000
                    readTimeout = 10000
                }

                val payload = JSONObject().apply {
                    put("module", moduleName)
                    put("data", telemetryData)
                    put("timestamp", System.currentTimeMillis())
                }.toString()

                connection.outputStream.use { os ->
                    val input = payload.toByteArray(Charsets.UTF_8)
                    os.write(input, 0, input.size)
                }

                val responseCode = connection.responseCode
                Log.d("Telemetry", "Response Code: $responseCode")
            } catch (e: Exception) {
                Log.e("Telemetry", "Error sending telemetry", e)
            } finally {
                connection?.disconnect()
            }
        }.start()
    }
}
