[app]

# 应用元数据
title = 金木注册工具
package.name = jinmuregister
package.domain = org.jinmu

source.dir = .
source.include_exts = py

version = 1.0
orientation = portrait
fullscreen = 0

# 入口点 - 使用重命名后的 main.py
entrypoint = main.py

# 依赖库 - 无Kivy，纯后台服务
# 注意：pycryptodome 可能需要特殊处理
requirements = python3, hostpython3, requests, pycryptodome, cython==0.29.36

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a
android.accept_sdk_license = True

# 日志和调试
log_level = 2
android.logcat_filters = *:D

# 优化配置
android.wakelock = True
android.allow_backup = False

# 关键修复：解决 Cython 编译问题
p4a.branch = master
p4a.commit = 2023.08.17
p4a.recommended_ndk_api = 21
android.enable_androidx = True
python.version = 3.9.9
python.allow_jni = 0
