@echo off
chcp 65001 >nul
echo ============================================
echo   华仔音乐盒 Android APK 打包工具
echo ============================================
echo.

REM 检查 Docker 是否运行
echo [1/4] 检查 Docker 状态...
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未运行，正在启动 Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo ⏳ 等待 Docker 启动 (60秒)...
    timeout /t 60 /nobreak >nul
    
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe" ps >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Docker 启动失败，请手动启动 Docker Desktop 后重试
        pause
        exit /b 1
    )
)
echo ✅ Docker 运行正常

REM 检查镜像
echo.
echo [2/4] 检查 Buildozer 镜像...
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect kivy/buildozer >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ 首次运行需要下载打包镜像 (~2GB)，请耐心等待...
    echo    如果下载中断，请重新运行此脚本（会自动续传）
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe" pull kivy/buildozer
    if %errorlevel% neq 0 (
        echo ❌ 镜像下载失败，请检查网络后重试
        pause
        exit /b 1
    )
)
echo ✅ Buildozer 镜像就绪

REM 执行打包
echo.
echo [3/4] 开始打包 APK...
echo    首次打包需要下载 Android SDK (~1.5GB)
echo    后续打包会快很多
echo.

"C:\Program Files\Docker\Docker\resources\bin\docker.exe" run --rm ^
    -e BUILDOZER_WARN_ON_ROOT=1 ^
    -v "%~dp0:/app" ^
    -w /app ^
    kivy/buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo ✅ 打包成功！
    echo.
    
    REM 查找生成的 APK
    for /r "%~dp0bin" %%f in (*.apk) do (
        echo 📱 APK 文件: %%f
        echo.
        echo 💡 将 APK 传输到手机安装即可
    )
    
    REM 打开 bin 目录
    if exist "%~dp0bin" explorer "%~dp0bin"
) else (
    echo.
    echo ❌ 打包失败，请检查错误信息
)

echo.
echo [4/4] 完成
pause
