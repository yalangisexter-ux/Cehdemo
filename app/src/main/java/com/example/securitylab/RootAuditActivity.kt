package com.example.securitylab

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class RootAuditActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Trigger telemetry when a root/binary audit detects an issue
        TelemetryClient.sendData("rootaudit", "root_binary_detected_su_path_found")
    }
}
