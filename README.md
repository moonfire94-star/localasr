# LocalASR - 本地语音识别工具

基于 SenseVoice 模型的实时语音识别和离线文件转写工具，支持中文、英文、粤语等多种语言。无需联网，完全本地运行。

## 🎯 项目特点

- ✅ **完全本地运行**：无需联网，保护隐私
- ✅ **实时语音识别**：支持麦克风实时语音转文字
- ✅ **离线文件转写**：支持拖拽 MP3/WAV 文件进行语音识别
- ✅ **GPU 加速**：自动检测并使用 NVIDIA GPU 加速识别
- ✅ **多语言支持**：中文（普通话）、粤语、英文、日文、韩文
- ✅ **窗口置顶**：可设置窗口始终置顶，方便使用
- ✅ **独立运行**：打包后可独立运行，无需安装 Python 环境

## 🛠️ 环境要求

- **操作系统**：Windows 10/11
- **Python**：3.8+（仅开发时需要）
- **硬件**：推荐 NVIDIA GPU（用于加速识别）

## 📦 快速开始

### 方法一：使用打包版本（推荐）

1. **下载发布版本**：从 Release 页面下载 `LocalASR.zip`
2. **解压运行**：解压后双击 `LocalASR.exe` 运行
3. **开始使用**：
   - 点击 "🎙️ 开启实时识别" 进行实时语音识别
   - 拖拽 MP3/WAV 文件到窗口进行离线转写

### 方法二：源码运行

1. **克隆项目**：
   ```bash
   git clone https://github.com/yourusername/localasr.git
   cd localasr
   ```

2. **激活虚拟环境**：
   ```bash
   .venv\Scripts\activate
   ```

3. **运行应用**：
   ```bash
   python main_app.py
   ```

### 方法三：自行打包

1. **安装依赖**：
   ```bash
   pip install pyinstaller
   ```

2. **运行打包脚本**：
   ```bash
   python build.py
   ```

3. **打包完成后**：可执行文件在 `dist/LocalASR/LocalASR.exe`

## 🎯 使用方法

### 实时语音识别

1. 点击 "🎙️ 开启实时识别" 按钮
2. 对着麦克风说话
3. 识别结果会实时显示在界面上
4. 点击 "🛑 停止识别" 结束识别

### 离线文件转写

1. 拖拽 MP3/WAV 文件到应用窗口
2. 程序会自动进行语音识别
3. 转写结果显示在界面上

### 窗口置顶

点击 "📌 置顶窗口" 按钮，可设置窗口始终置顶，方便边录音边看结果。

## 📁 项目结构

```
localasr/
├── main_app.py          # 主应用程序
├── build.py             # 打包脚本
├── build.bat            # 打包批处理文件
├── run.bat              # 运行脚本
├── bin/                 # 服务器可执行文件
│   ├── sherpa-onnx-microphone.exe          # 实时识别服务器
│   ├── sherpa-onnx-offline-websocket-server.exe  # 离线转写服务器
│   └── ...
├── model/               # 完整模型（离线转写使用）
│   ├── model.onnx
│   └── tokens.txt
├── model_mini/          # 小型模型（实时识别使用）
│   ├── encoder.int8.onnx
│   ├── decoder.int8.onnx
│   └── tokens.txt
└── .venv/               # 虚拟环境
```

## ⚙️ 技术配置

### 实时识别配置
- **模型**：使用小型模型保证低延迟
- **解码方法**：`modified_beam_search` 提高准确率
- **端点检测**：优化静音检测阈值，减少误识别
- **GPU 加速**：自动检测并使用 GPU 加速

### 离线转写配置
- **模型**：使用完整模型提高识别准确率
- **GPU 加速**：支持 CUDA 加速识别

## 🔧 常见问题

### 1. 实时识别过于灵敏
- **原因**：默认的端点检测阈值过低
- **解决**：已在代码中优化了端点检测参数

### 2. 识别不准确
- **原因**：使用的是小型模型，准确率有限
- **解决**：可在代码中修改为使用完整模型（修改 `record_loop` 函数中的模型路径）

### 3. GPU 加速不工作
- **原因**：可能缺少 CUDA 驱动或服务器不支持 GPU
- **解决**：会自动回退到 CPU 模式，不影响使用

### 4. 服务器启动失败
- **原因**：端口被占用或模型文件不存在
- **解决**：检查端口是否被占用，确保模型文件存在

### 5. 打包后运行显示配置信息
- **原因**：sherpa-onnx 服务器启动时会打印配置信息
- **解决**：已在代码中添加过滤逻辑，只显示真正的识别结果

## 🚀 性能优化

### 实时识别优化
- 使用小型模型保证低延迟
- GPU 加速提高处理速度
- 优化端点检测减少误识别

### 离线转写优化
- 使用完整模型提高准确率
- 支持大文件批量处理
- GPU 加速提高处理速度

## 📞 技术支持

如果遇到问题，请检查日志文件：
- `log_online.txt` - 在线服务日志
- `log_offline.txt` - 离线服务日志

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 📄 许可证

本项目基于 SenseVoice 模型和 sherpa-onnx 框架构建，遵循相应的开源许可证。

## 🙏 致谢

- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) - 语音识别模型
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) - 语音识别框架
- [PySide6](https://www.qt.io/qt-for-python) - GUI 框架
