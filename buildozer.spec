[app]
title = Khanjar
package.name = khanjar
package.domain = com.trading

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 5.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,plyer,numpy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,VIBRATE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 24
android.ndk = 25b
android.gradle_dependencies = com.google.android.material:material:1.9.0
android.enable_androidx = True

# صریحاً SDK و NDK رو مشخص می‌کنیم
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.accept_sdk_license = True

services = KhanjarService:service.py:foreground

android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
