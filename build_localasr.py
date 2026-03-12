import os
import sys
import subprocess

def build_exe():
    """构建 LocalASR 可执行文件"""
    print("开始打包 LocalASR 本地语音识别工具...")
    
    # 清理旧的构建文件
    print("清理目录: build")
    subprocess.run(['rmdir', '/s', '/q', 'build'], shell=True, check=False)
    print("清理目录: dist") 
    subprocess.run(['rmdir', '/s', '/q', 'dist'], shell=True, check=False)
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--name', 'LocalASR',
        '--onedir',  # 使用目录模式避免大小限制
        '--windowed',  # 无控制台窗口
        '--add-data', 'bin;bin',  # 包含bin目录
        '--add-data', 'model;model',  # 包含model目录
        '--add-data', 'model_mini;model_mini',  # 包含model_mini目录
        '--hidden-import', 'sounddevice',
        '--hidden-import', 'librosa',
        '--hidden-import', 'numpy',
        '--hidden-import', 'websocket',
        '--hidden-import', 'PySide6',
        '--exclude-module', 'setuptools',
        '--exclude-module', 'pkg_resources',
        'main_app_new.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ 打包完成！")
        print("📁 输出目录: dist/LocalASR/")
        print("🎯 可执行文件: dist/LocalASR/LocalASR.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

if __name__ == "__main__":
    if build_exe():
        print("\n🎉 LocalASR 打包成功！")
        print("📦 发布文件位置: dist/LocalASR/")
        print("🚀 双击 LocalASR.exe 即可运行")
    else:
        print("\n❌ 打包失败，请检查错误信息")
        sys.exit(1)