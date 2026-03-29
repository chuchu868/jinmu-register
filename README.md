# 金木注册工具

## 自动构建 APK

### 方法：GitHub Actions（最简单）

1. **Fork 或创建 GitHub 仓库**
   - 在 GitHub 创建新仓库
   - 上传所有文件到仓库

2. **触发自动构建**
   - 推送代码到 main 分支，或
   - 进入 Actions 页面，点击 "Run workflow"

3. **下载 APK**
   - 等待构建完成（约 15-30 分钟）
   - 在 Actions 页面下载 APK 文件

### 文件说明

- `simple_main.py` - 主程序
- `网页式金木自动注册.py` - 注册功能
- `buildozer.spec` - 打包配置
- `.github/workflows/build-apk.yml` - 自动构建配置

### 手动构建（可选）

如果有 Linux 环境：
```bash
pip install buildozer cython kivy
buildozer android debug
```

### 安装 APK

1. 下载 APK 文件
2. 允许 "未知来源" 安装
3. 安装并运行
