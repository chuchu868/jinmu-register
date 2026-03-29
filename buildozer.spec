[app]

title = 金木注册工具
package.name = jinmuregister
package.domain = org.jinmu

source.dir = .
source.include_exts = py

version = 1.0
orientation = portrait
fullscreen = 0

# 入口点 - 确保您的脚本已重命名为 main.py
entrypoint = main.py

# 依赖库
requirements = python3, hostpython3, requests, pycryptodome

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a  # 先只编译一个架构，减少复杂度
android.accept_sdk_license = True

# 关键修复：指定使用更新版本的 python-for-android
p4a.branch = develop
android.enable_androidx = True

# 日志级别
log_level = 2

# 性能优化
android.wakelock = True
android.allow_backup = False
