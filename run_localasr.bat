@echo off
echo 正在运行 LocalASR 本地语音识别工具...
echo.

REM 检查是否存在打包版本
if exist ".\.venv\Scripts\dist\LocalASR\LocalASR.exe" (
    echo 找到打包版本，正在启动...
    start "" ".\.venv\Scripts\dist\LocalASR\LocalASR.exe"
) else if exist ".\dist\LocalASR\LocalASR.exe" (
    echo 找到打包版本，正在启动...
    start "" ".\dist\LocalASR\LocalASR.exe"
) else (
    echo 未找到打包版本，尝试运行源码...
    if exist ".\.venv\Scripts\activate.bat" (
        echo 激活虚拟环境并运行...
        call .\.venv\Scripts\activate.bat
        python main_app_new.py
    ) else (
        echo 未找到虚拟环境，直接运行源码...
        python main_app_new.py
    )
)

echo.
echo LocalASR 已启动！
echo.
pause