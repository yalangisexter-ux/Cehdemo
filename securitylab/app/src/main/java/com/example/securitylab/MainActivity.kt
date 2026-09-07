package com.example.securitylab

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import com.example.securitylab.worker.StealthSyncWorker
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tvStatus = findViewById<TextView>(R.id.tvStatus)

        val workRequest = PeriodicWorkRequestBuilder<StealthSyncWorker>(15, TimeUnit.MINUTES).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "StealthSyncJob",
            ExistingPeriodicWorkPolicy.KEEP,
            workRequest
        )

        tvStatus.text = "WorkManager periodic sync registered successfully.\nPolling loop armed."

        findViewById<Button>(R.id.btnForceWork).setOnClickListener {
            StealthSyncWorker.executeSyncNow(applicationContext)
            tvStatus.text = "Immediate synchronization cycle dispatched."
        }
    }
}
