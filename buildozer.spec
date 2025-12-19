[app]
title = Khanjar Supreme
package.name = khanjar
package.domain = org.supreme

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 5.0

requirements = python3,kivy==2.2.1,requests,numpy,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE,FOREGROUND_SERVICE,WAKE_LOCK

android.api = 31
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

android.gradle_dependencies = androidx.core:core:1.6.0,androidx.appcompat:appcompat:1.3.1

services = KhanjarService:service.py:foreground

[buildozer]
log_level = 2
warn_on_root = 1
