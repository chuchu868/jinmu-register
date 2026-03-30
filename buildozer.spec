[app]

title = JinmuRegister
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

p4a.branch = develop
p4a.fork = kivy

android.skip_update = False
