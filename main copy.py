'''
Author: Diana Tang
Date: 2024-10-17 14:54:19
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/main.py
'''
import subprocess

# 输入视频和字幕文件的路径
input_video = "input.mp4"
input_subtitle = "subtitles.srt"
output_video = "output_with_subtitles.mp4"

# FFmpeg命令，将字幕合并到视频中
command = [
    "ffmpeg",
    "-i", input_video,
    "-vf", f"subtitles={input_subtitle}",
    output_video
]

# 运行命令
subprocess.run(command)
