package com.example.securitylab

import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val testButton = findViewById<Button>(R.id.testButton)
        testButton.setOnClickListener {
            // Trigger a test telemetry event from the UI
            TelemetryClient.sendData("attacker", "button_clicked_telemetry_test")
        }
    }
}
