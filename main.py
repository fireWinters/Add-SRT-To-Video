'''
Author: Diana Tang
Date: 2024-10-17 14:54:19
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/main.py
'''



import os
import cv2
import whisper
import moviepy.editor as mp
import subprocess

# 设置文件路径
video_path = "./videos/绪论1中文.mp4"
audio_path = "./videos/1.1.wav"
output_video_path = "./videos/绪论1有字幕cv.mp4"
final_output_path="./videos/绪论1有字幕音频cv.mp4"
subtitle_path = "./videos/subtitles.srt"

# 提取视频中的原始音频并保存为最终合并用的音频
original_audio_path = "audio_original.wav"
command = [
    "ffmpeg",
    "-i", video_path,
    "-q:a", "0",
    "-map", "a",
    "-y",
    original_audio_path
]
subprocess.run(command)

# 加载 Whisper 模型
model = whisper.load_model("base")

# 使用 Whisper 进行语音识别
result = model.transcribe(audio_path)

# 生成 SRT 字幕文件
def generate_srt_file(subtitle_path, segments):
    os.makedirs(os.path.dirname(subtitle_path), exist_ok=True)
    if not segments:
        print("未识别到任何内容，字幕文件将为空。")
    with open(subtitle_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"].strip()

            if not text:
                continue

            # 格式化时间戳
            start_hours, start_remainder = divmod(start_time, 3600)
            start_minutes, start_seconds = divmod(start_remainder, 60)
            start_milliseconds = int((start_seconds % 1) * 1000)
            start_seconds = int(start_seconds)

            end_hours, end_remainder = divmod(end_time, 3600)
            end_minutes, end_seconds = divmod(end_remainder, 60)
            end_milliseconds = int((end_seconds % 1) * 1000)
            end_seconds = int(end_seconds)

            f.write(f"{i + 1}\n")
            f.write(f"{int(start_hours):02}:{int(start_minutes):02}:{int(start_seconds):02},{start_milliseconds:03} --> {int(end_hours):02}:{int(end_minutes):02}:{int(end_seconds):02},{end_milliseconds:03}\n")
            f.write(f"{text}\n\n")

# 调用生成 SRT 文件的函数
generate_srt_file(subtitle_path, result["segments"])

# 打开视频并逐帧处理
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

current_frame = 0
current_text = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 计算当前帧对应的时间（秒）
    current_time = current_frame / fps

    # 查找当前时间的字幕内容
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]

        if start_time <= current_time <= end_time:
            current_text = segment["text"].strip()
            break
        else:
            current_text = ""

    # 在当前帧上显示字幕
    if current_text:
        cv2.putText(frame, current_text, (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA, False)

    # 写入处理后的帧
    out.write(frame)
    current_frame += 1

cap.release()
out.release()

# 使用 ffmpeg 将原始音频添加到最终输出视频中
command = [
    "ffmpeg",
    "-i", output_video_path,   # 输入处理过的视频
    "-i", original_audio_path,  # 输入原始音频
    "-c:v", "copy",            # 复制视频流，不重新编码
    "-c:a", "aac",             # 使用 AAC 编码音频
    "-b:a", "192k",            # 设置音频比特率
    "-y",                       # 如果文件已存在则覆盖
    final_output_path            # 输出带有音频的视频
]
subprocess.run(command)

print(f"字幕已取得并保存为 {final_output_path}")

