[app]
title = 管控查询
package.name = pollution_query
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,csv
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.permissions = INTERNET, CALL_PHONE

[buildozer]
log_level = 2
warn_on_root = 0