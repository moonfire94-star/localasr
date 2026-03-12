@echo off

:: SenseVoice AI 语音助手启动脚本

echo =============================
echo SenseVoice AI 语音助手
 echo =============================
echo.

echo 正在启动应用...

:: 检查虚拟环境
if exist ".venv\Scripts\activate.bat" (
    echo 激活虚拟环境...
    call ".venv\Scripts\activate.bat"
) else (
    echo 警告: 虚拟环境不存在，尝试直接运行...
)

:: 运行应用
echo 启动主应用...
python main_app.py

:: 暂停以查看错误
if %errorlevel% neq 0 (
    echo 应用启动失败，请检查错误信息
    pause
)
