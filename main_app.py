import sys
import os
import json
import threading
import subprocess
import time
import tempfile
import librosa
import wave
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QHBoxLayout)
from PySide6.QtCore import Qt, Signal, QObject, QSize, Slot
from PySide6.QtGui import QTextCursor

# 信号类，用于线程间通信
class WorkerSignals(QObject):
    update_text = Signal(str)
    status_msg = Signal(str)

class SenseVoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SenseVoice AI 语音助手 (全功能优化版)")
        self.setFixedSize(QSize(550, 650))
        self.signals = WorkerSignals()
        self.signals.update_text.connect(self.on_update_text)
        self.signals.status_msg.connect(self.on_status_msg)
        
        self.is_recording = False
        self.asr_process = None 
        
        self.init_ui()
        self.setAcceptDrops(True) # 开启拖拽支持

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        self.status_label = QLabel("🔘 准备就绪 (支持拖拽离线识别 & 实时流刷新)")
        self.status_label.setStyleSheet("color: #444; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        self.caption_display = QTextEdit()
        self.caption_display.setReadOnly(True)
        self.caption_display.setStyleSheet("""
            background-color: #000; 
            color: #00FF00; 
            font-family: 'Microsoft YaHei'; 
            font-size: 18px; 
            line-height: 1.5;
        """)
        layout.addWidget(self.caption_display)
        
        ctrl_layout = QHBoxLayout()
        self.mic_btn = QPushButton("🎙️ 开启实时识别")
        self.mic_btn.setMinimumHeight(50)
        self.mic_btn.setStyleSheet("background-color: #5cb85c; color: white; font-weight: bold;")
        self.mic_btn.clicked.connect(self.toggle_mic)
        
        self.pin_btn = QPushButton("📌 置顶窗口")
        self.pin_btn.setCheckable(True)
        self.pin_btn.clicked.connect(self.toggle_pin)
        
        ctrl_layout.addWidget(self.mic_btn)
        ctrl_layout.addWidget(self.pin_btn)
        layout.addLayout(ctrl_layout)
        
        self.drop_area = QLabel("\n\n📥 拖拽音频文件至此 (SenseVoice GPU 离线加速)\n\n")
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.drop_area.setStyleSheet("border: 2px dashed #AAA; color: #777; margin-top: 10px;")
        layout.addWidget(self.drop_area)
        
        self.setCentralWidget(central_widget)

    # --- 实时识别部分 ---
    def toggle_mic(self):
        if not self.is_recording:
            self.is_recording = True
            self.mic_btn.setText("🛑 停止识别 (正在听...)")
            self.mic_btn.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold;")
            threading.Thread(target=self.record_loop, daemon=True).start()
        else:
            self.is_recording = False
            self.mic_btn.setText("🎙️ 开启实时识别")
            self.mic_btn.setStyleSheet("background-color: #5cb85c; color: white; font-weight: bold;")
            if self.asr_process:
                try:
                    self.asr_process.terminate()
                    self.asr_process.kill()
                except: pass
                self.asr_process = None

    def record_loop(self):
        # 获取应用程序所在目录，支持pyinstaller打包
        if hasattr(sys, '_MEIPASS'):
            # 打包后运行
            base_dir = sys._MEIPASS
        else:
            # 开发模式运行
            base_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(base_dir, "bin", "sherpa-onnx-microphone.exe")
        cmd = [
            exe_path,
            f"--paraformer-encoder={os.path.join(base_dir, 'model_mini', 'encoder.int8.onnx')}",
            f"--paraformer-decoder={os.path.join(base_dir, 'model_mini', 'decoder.int8.onnx')}",
            f"--tokens={os.path.join(base_dir, 'model_mini', 'tokens.txt')}",
            "--provider=cuda",
            "--num-threads=1"
        ]
        try:
            self.asr_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8', errors='replace', bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            full_history = []
            current_temp = ""
            last_update_time = time.time()

            while self.is_recording and self.asr_process.poll() is None:
                line = self.asr_process.stdout.readline()
                if not line: break
                line = line.strip()
                
                # 过滤掉配置信息和调试输出
                if (line.startswith("OnlineRecognizerConfig") or 
                    line.startswith("OnlineModelConfig") or 
                    line.startswith("ProviderConfig") or
                    line.startswith("CudaConfig") or
                    line.startswith("TensorrtConfig") or
                    line.startswith("OnlineLMConfig") or
                    line.startswith("EndpointConfig") or
                    line.startswith("EndpointRule") or
                    line.startswith("OnlineCtcFstDecoderConfig") or
                    line.startswith("HomophoneReplacerConfig") or
                    ("=" in line and len(line) > 200)):  # 过滤长配置行
                    continue
                    
                if ":" in line and "csrc" not in line:
                    parts = line.split(":", 1)
                    content = parts[1].strip()
                    if content and "Realtek" not in content and not content.isdigit():
                        current_temp = content
                        last_update_time = time.time()
                        display_text = "\n".join(full_history) + ("\n" if full_history else "") + current_temp
                        self.signals.update_text.emit(display_text)

                if current_temp and (time.time() - last_update_time > 1.2):
                    full_history.append(current_temp + "。")
                    current_temp = ""
                    self.signals.update_text.emit("\n".join(full_history))
        finally:
            if self.asr_process:
                self.asr_process.kill()

    # --- 离线识别部分 (恢复原有功能) ---
    def process_offline(self, path):
        filename = os.path.basename(path)
        self.signals.status_msg.emit(f"🚀 GPU 解析中: {filename}")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        exe_path = os.path.join(base_dir, "bin", "sherpa-onnx-offline.exe")
        model_path = os.path.join(base_dir, "model", "model.onnx")
        tokens_path = os.path.join(base_dir, "model", "tokens.txt")
        
        wav_path = self.convert_to_wav_16k(path)
        if not wav_path:
            self.signals.status_msg.emit("❌ 音频格式转换失败")
            return

        cmd = [
            exe_path,
            f"--sense-voice-model={model_path}",
            f"--tokens={tokens_path}",
            "--provider=cuda",
            "--num-threads=1",
            os.path.abspath(wav_path)
        ]

        try:
            start_t = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', 
                                  errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
            
            if result.returncode == 0:
                final_text = ""
                for line in (result.stdout + result.stderr).split('\n'):
                    if '"text":' in line.strip() and line.strip().startswith('{'):
                        try:
                            final_text = json.loads(line.strip()).get("text", "")
                            if final_text: break
                        except: continue
                
                cost = round(time.time() - start_t, 2)
                if final_text:
                    self.signals.update_text.emit(f"\n[文件识别结果 | {cost}s]:\n{final_text}\n")
                    self.signals.status_msg.emit(f"✅ 解析成功 ({cost}s)")
                else:
                    self.signals.status_msg.emit("⚠️ 识别结束，但未解析出文本")
        except Exception as e:
            self.signals.status_msg.emit(f"❌ 运行异常: {e}")
        finally:
            if wav_path and os.path.exists(wav_path):
                try: os.remove(wav_path)
                except: pass

    def convert_to_wav_16k(self, input_path):
        try:
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_wav.close()
            audio, _ = librosa.load(input_path, sr=16000, mono=True)
            with wave.open(temp_wav.name, 'wb') as f:
                f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000)
                f.writeframes((audio * 32767).astype(np.int16).tobytes())
            return temp_wav.name
        except: return None

    @Slot(str)
    def on_update_text(self, text):
        self.caption_display.setPlainText(text)
        self.caption_display.moveCursor(QTextCursor.End)

    def on_status_msg(self, msg):
        self.status_label.setText(msg)

    def toggle_pin(self, checked):
        if checked: self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else: self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            f = url.toLocalFile()
            if f.lower().endswith(('.mp3', '.wav', '.flac')):
                threading.Thread(target=self.process_offline, args=(f,), daemon=True).start()

    def stop_asr_process(self):
        """统一强杀函数：确保后台不留活口"""
        self.is_recording = False
        if self.asr_process:
            try:
                # 1. 尝试正常终止
                self.asr_process.terminate()
                # 2. Windows 命令行强杀 PID 树
                subprocess.run(f"taskkill /F /T /PID {self.asr_process.pid}", 
                               shell=True, capture_output=True)
            except:
                pass
            self.asr_process = None
        
    def closeEvent(self, event):
        """窗口关闭时彻底清理"""
        self.stop_asr_process()
        # 兜底：如果还有同名进程残留，直接根据映像名称清场
        subprocess.run("taskkill /F /IM sherpa-onnx-microphone.exe /T", 
                       shell=True, capture_output=True)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SenseVoiceApp()
    window.show()
    sys.exit(app.exec())