package com.example.securitylab

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class AttackerActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Trigger telemetry when a simulated exfiltration event occurs
        TelemetryClient.sendData("attacker", "exfiltration_payload_transmitted")
    }
}
