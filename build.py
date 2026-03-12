#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SenseVoice AI 语音助手打包脚本

使用方法：
1. 确保网络连接正常
2. 安装pyinstaller: pip install pyinstaller
3. 运行此脚本: python build.py
"""

import os
import shutil
import subprocess
import sys

def clean_build():
    """清理之前的构建文件"""
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)

def build_exe():
    """使用pyinstaller打包应用"""
    print("开始打包SenseVoice AI语音助手...")
    
    # 检查pyinstaller是否安装
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("错误: pyinstaller未安装，请先运行: pip install pyinstaller")
        return False
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--name', 'SenseVoiceAI',
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
        'main_app.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功！")
        print(f"可执行文件位置: dist/SenseVoiceAI.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e.stderr}")
        return False

def create_portable_package():
    """创建便携版包"""
    if not os.path.exists('dist/SenseVoiceAI.exe'):
        print("错误: 可执行文件不存在，请先运行build_exe()")
        return False
    
    print("创建便携版包...")
    
    # 创建便携版目录
    portable_dir = 'SenseVoiceAI_Portable'
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # 复制必要文件
    files_to_copy = [
        'dist/SenseVoiceAI.exe',
        'bin',
        'model',
        'model_mini'
    ]
    
    for item in files_to_copy:
        dest = os.path.join(portable_dir, os.path.basename(item))
        if os.path.isdir(item):
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
        print(f"复制: {item} -> {dest}")
    
    print("便携版包创建完成！")
    print(f"位置: {portable_dir}")
    return True

if __name__ == '__main__':
    clean_build()
    if build_exe():
        create_portable_package()
    print("\n打包完成！")
