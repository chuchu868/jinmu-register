[app]
title = 金木注册工具
package.name = jinmu_register
package.domain = com.jinmu.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 1.0.0
requirements = python3,kivy,requests,pycryptodome
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
orientation = portrait
fullscreen = 0
android.entrypoint = simple_main.py

[buildozer]
log_level = 2
warn_on_root = 1
