[app]

# 应用元数据
title = 金木注册工具
package.name = jinmuregister
package.domain = org.jinmu

source.dir = .
source.include_exts = py  # 只包含Python脚本，如有其他资源文件请添加扩展名

version = 1.0
orientation = portrait
fullscreen = 0

# ！！！关键修复：指定无图形界面的主脚本
# 将主脚本重命名为英文，避免编码问题
# 请先将“网页式金木自动注册.py”文件重命名为“main.py”
entrypoint = main.py

# 依赖库
# 移除了“kivy”，因为无界面应用不需要它
# 保留requests和pycryptodome，它们是您脚本的核心功能依赖
requirements = python3, hostpython3, requests, pycryptodome

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33  # 【已修复】与 android.api 保持一致
android.ndk = 25b
android.arch = armeabi-v7a, arm64-v8a
android.accept_sdk_license = True

# 日志和调试
log_level = 2
android.logcat_filters = *:D

# 优化配置
android.wakelock = True  # 防止CPU休眠，适用于后台服务
android.allow_backup = False
