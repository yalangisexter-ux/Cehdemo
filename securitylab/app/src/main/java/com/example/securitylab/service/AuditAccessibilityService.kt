package com.example.securitylab.service

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import android.util.Log

class AuditAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            rootInActiveWindow?.let {
                traverseNodes(it)
                it.recycle()
            }
        }
    }

    private fun traverseNodes(node: AccessibilityNodeInfo) {
        val text = node.text?.toString()
        if (!text.isNullOrBlank()) {
            Log.d("A11yAudit", "Detected Node Text: $text")
        }
        for (i in 0 until node.childCount) {
            node.getChild(i)?.let {
                traverseNodes(it)
                it.recycle()
            }
        }
    }

    override fun onInterrupt() {}
}
