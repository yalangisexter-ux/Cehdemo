
package com.example.stealth

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import android.util.Log

class BackgroundMonitorService : Service(), LocationListener {
    private lateinit var locationManager: LocationManager

    override fun onCreate() {
        super.onCreate()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel("monitor_channel", "Background Monitor", NotificationManager.IMPORTANCE_LOW)
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
        locationManager = getSystemService(LOCATION_SERVICE) as LocationManager
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0f, this)
    }

    override fun onLocationChanged(location: Location?) {
        location?.let {
            Log.d("STEALTH", "Lat: ${it.latitude}, Lon: ${it.longitude}")
        }
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
