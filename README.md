# 华仔音乐盒 Android 版本

## 打包说明

### 方法一：使用 GitHub Actions（推荐，免费）

1. 将整个 `华仔音乐盒_android` 文件夹上传到 GitHub 仓库
2. 创建 `.github/workflows/build.yml` 文件：

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install Buildozer
      run: |
        pip install buildozer
        pip install cython
    
    - name: Build APK
      run: buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: huazaimusicbox-apk
        path: bin/*.apk
```

3. 推送代码后，GitHub Actions 会自动构建 APK
4. 构建完成后在 Actions -> Artifacts 中下载 APK

---

### 方法二：本地打包（需要 Linux 环境）

**前提条件：**
- Ubuntu 20.04+ 或 WSL2（Windows子系统Linux）
- Python 3.9+

**打包步骤：**

```bash
# 1. 安装依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake

# 2. 安装 Python 依赖
pip3 install --upgrade pip
pip3 install buildozer cython

# 3. 进入项目目录
cd 华仔音乐盒_android

# 4. 首次打包（会自动下载 SDK/NDK，需要较长时间）
buildozer android debug

# 5. 后续打包（增量构建，速度更快）
buildozer android debug
```

**打包完成后，APK 文件在 `bin/` 目录下**

---

### 方法三：使用 Docker（跨平台）

```bash
# 1. 拉取 Kivy 打包镜像
docker pull kivy/buildozer

# 2. 运行打包
docker run --rm -v "E:\下载\QClaw\resources\openclaw\config\skills\华仔音乐盒_android":/app kivy/buildozer android debug
```

---

## 功能特性

- ✅ 6大音乐源：网易云、酷狗、QQ音乐、酷我、咪咕
- ✅ 全网搜索：同时搜索所有平台
- ✅ 天蓝色清新界面
- ✅ 在线播放
- ✅ 热门标签快速搜索

## 安装说明

1. 将 APK 传输到 Android 手机
2. 开启"允许安装未知来源应用"
3. 点击 APK 安装
4. 首次运行需要授权网络和存储权限

## 系统要求

- Android 5.0+ (API 21+)
- 需要网络权限
- 建议存储空间 50MB+
