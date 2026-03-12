@echo off

echo SenseVoice AI 语音助手打包工具
echo =============================
echo.

echo 1. 安装pyinstaller
echo 2. 运行打包脚本
echo 3. 退出

echo.
set /p choice=请选择操作: 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto build
if "%choice%"=="3" goto exit

echo 无效选择，请重新运行
pause
goto end

:install
echo 正在安装pyinstaller...
pip install pyinstaller
echo 安装完成！
pause
goto end

:build
echo 正在运行打包脚本...
python build.py
echo 打包完成！
pause
goto end

:exit
echo 退出...
goto end

:end
