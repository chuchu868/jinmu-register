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

android.extract_native_libs = False
android.enable_androidx = True
android.allow_backup = False
android.wakelock = True

log_level = 2

android.gradle_properties = 
    org.gradle.jvmargs=-Xmx4g -Dfile.encoding=UTF-8
    org.gradle.parallel=true
    org.gradle.caching=true
    org.gradle.configureondemand=true
    org.gradle.daemon=false
    android.useAndroidX=true
    android.enableJetifier=false
    android.enableR8=true
