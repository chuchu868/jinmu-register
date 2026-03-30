[app]

# 应用元数据
title = JinmuRegister
package.name = jinmuregister
package.domain = org.jinmu

source.dir = .
source.include_exts = py

version = 1.0
orientation = portrait
fullscreen = 0

# 入口点
entrypoint = main.py

# 精简依赖：只保留最核心的库
# 移除了 Kivy 和 pyjnius 相关依赖
requirements = python3, hostpython3, requests, pycryptodome

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# 日志级别
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
