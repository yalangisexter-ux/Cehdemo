package com.example.securitylab

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class DefenderActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Trigger telemetry when a defense/scan event occurs
        TelemetryClient.sendData("defender", "system_integrity_verified")
    }
}
