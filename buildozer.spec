[app]

title = 金木注册工具
package.name = jinmuregister
package.domain = org.jinmu

source.dir = .
source.include_exts = py

version = 1.0
orientation = portrait
fullscreen = 0

entrypoint = main.py

requirements = python3, hostpython3, requests, pycryptodome

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.accept_sdk_license = True

log_level = 2
android.logcat_filters = *:D

android.wakelock = True
android.allow_backup = False

p4a.branch = develop
android.enable_androidx = True
