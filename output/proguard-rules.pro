
-keepclassmembers class * {{
    public <init>(android.content.Context);
}}
-dontpreverify
-repackageclasses ''
-allowaccessmodification
-optimizations !code/simplification/arithmetic,!field/*,!class/merging/*
-keepattributes Signature,Exception,InnerClasses,EnclosingMethod
-keep class com.**.** **;
-keep class android.** {{
    public *;
}}
