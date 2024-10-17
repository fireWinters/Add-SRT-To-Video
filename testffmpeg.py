'''
Author: Diana Tang
Date: 2024-10-17 15:31:52
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/testffmpeg.py
'''
import subprocess

def check_ffmpeg():
    try:
        # 使用 subprocess 运行 "ffmpeg -version" 命令来检查 ffmpeg 是否存在
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("FFmpeg is installed and available.")
        else:
            print("FFmpeg is not installed or not in the system path.")
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in the system path.")

check_ffmpeg()
import shutil

ffmpeg_path = shutil.which("ffmpeg")

if ffmpeg_path:
    print(f"FFmpeg path: {ffmpeg_path}")
else:
    print("FFmpeg is not installed or not in the system path.")

