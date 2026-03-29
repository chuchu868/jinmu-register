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

# 确保主脚本名为 main.py
entrypoint = main.py

# 依赖库 - 移除有问题的版本限制
requirements = python3, hostpython3, requests, pycryptodome

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
# 修复：使用正确的配置名
android.arch = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

# 日志和调试
log_level = 2
android.logcat_filters = *:D

# 优化配置
android.wakelock = True
android.allow_backup = False

# 关键修复：移除有问题的版本指定，让Buildozer自动选择
# 注释掉可能引起问题的 p4a.commit
# p4a.commit = 2023.08.17
# p4a.branch = master

# 启用 androidx
android.enable_androidx = True
