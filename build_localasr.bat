@echo off
echo 正在打包 LocalASR 本地语音识别工具...
echo.

REM 清理旧的构建文件
echo 清理构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 运行打包
echo 开始打包...
cd .venv\Scripts
pyinstaller --name LocalASR --onedir --windowed --add-data "..\..\bin;bin" --add-data "..\..\model;model" --add-data "..\..\model_mini;model_mini" --hidden-import sounddevice --hidden-import librosa --hidden-import numpy --hidden-import websocket --hidden-import PySide6 --exclude-module setuptools --exclude-module pkg_resources ..\..\main_app_new.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ LocalASR 打包成功！
    echo 📁 输出目录: .venv\Scripts\dist\LocalASR\
    echo 🎯 可执行文件: .venv\Scripts\dist\LocalASR\LocalASR.exe
    echo.
    echo 🎉 打包完成！
) else (
    echo.
    echo ❌ 打包失败，请检查错误信息
    pause
    exit /b 1
)

pause