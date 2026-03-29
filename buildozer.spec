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

# 依赖库 - 精简版本，减少构建复杂度
requirements = python3, hostpython3, requests, pycryptodome

# Android 配置
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a  # 先只编译一个架构
android.accept_sdk_license = True

# Gradle 配置修复
android.gradle_dependencies = ''
android.add_gradle_repositories = ''
android.enable_androidx = True
android.allow_backup = False
android.wakelock = True

# 构建优化
log_level = 2
android.logcat_filters = *:D

# 修复 Gradle 版本问题
android.gradle_version = 7.3.0
android.build_tools_version = 33.0.0
