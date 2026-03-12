@echo off
chcp 65001

cd /d %~dp0

:: 1. 启动流式服务 (用于实时字幕) - 端口 6006
start "实时流-Paraformer" .\sherpa-onnx-online-websocket-server.exe ^
  --port=6006 ^
  --paraformer-encoder="./model_mini/encoder.int8.onnx" ^
  --paraformer-decoder="./model_mini/decoder.int8.onnx" ^
  --tokens="./model_mini/tokens.txt" ^
  --num-threads=2

:: 2. 启动离线服务 (用于 MP3 文件) - 端口 6007
start "离线转写-SenseVoice" .\sherpa-onnx-offline-websocket-server.exe ^
  --port=6007 ^
  --sense-voice-model="./model/model.onnx" ^
  --tokens="./model/tokens.txt" ^
  --num-threads=4

echo [服务启动就绪] 
echo 实时字幕请连接 6006，文件解析请连接 6007。
pause