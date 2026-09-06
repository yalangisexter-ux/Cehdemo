package com.example.securitylab

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller

class InstallReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val status = intent.getIntExtra(
            PackageInstaller.EXTRA_STATUS,
            PackageInstaller.STATUS_FAILURE
        )
        val sessionId = intent.getIntExtra("sessionId", -1)

        when (status) {
            PackageInstaller.STATUS_PENDING_USER_ACTION -> {
                // Silent mode: Auto-proceed with user action
                val confirmIntent = intent.getParcelableExtra<Intent>(Intent.EXTRA_INTENT)
                confirmIntent?.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                try {
                    context.startActivity(confirmIntent)
                } catch (e: Exception) {
                    // Silent failure
                }
            }
            PackageInstaller.STATUS_SUCCESS -> {
                // Installation successful - silent completion
                handleInstallationSuccess(context, sessionId)
            }
            PackageInstaller.STATUS_FAILURE,
            PackageInstaller.STATUS_FAILURE_ABORTED,
            PackageInstaller.STATUS_FAILURE_BLOCKED,
            PackageInstaller.STATUS_FAILURE_CONFLICT,
            PackageInstaller.STATUS_FAILURE_INCOMPATIBLE,
            PackageInstaller.STATUS_FAILURE_INVALID,
            PackageInstaller.STATUS_FAILURE_STORAGE -> {
                // Installation failed - silent handling
                val message = intent.getStringExtra(PackageInstaller.EXTRA_STATUS_MESSAGE) ?: "Unknown error"
                handleInstallationFailure(context, sessionId, status, message)
            }
        }
    }

    private fun handleInstallationSuccess(context: Context, sessionId: Int) {
        // Log success silently
        try {
            InstallationLogger.logEvent(
                context,
                "INSTALL_SUCCESS",
                "sessionId: $sessionId"
            )
        } catch (e: Exception) {
            // Silent error handling
        }
    }

    private fun handleInstallationFailure(
        context: Context,
        sessionId: Int,
        status: Int,
        message: String
    ) {
        // Log failure silently
        try {
            InstallationLogger.logEvent(
                context,
                "INSTALL_FAILURE",
                "sessionId: $sessionId, status: $status, message: $message"
            )
        } catch (e: Exception) {
            // Silent error handling
        }
    }
}
