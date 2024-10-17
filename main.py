'''
Author: Diana Tang
Date: 2024-10-17 14:54:19
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/main.py
'''


import os
import cv2
import wave
import json
import moviepy.editor as mp
from vosk import Model, KaldiRecognizer
import subprocess


# 设置文件路径
video_path = "./videos/绪论1中文.mp4"
audio_path = "./videos/1.wav"
model_path = "./models/vosk-model-small-cn-0.22"  # Vosk 中文模型的路径
output_video_path = "./videos/绪论1有字幕.mp4"

# 提取视频中的音频并保存为 WAV 格式
video = mp.VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

# 使用 ffmpeg 提取音频并转换为 16kHz、单声道的 WAV 格式
command = [
    "ffmpeg",
    "-i", video_path,          # 输入文件
    "-ac", "1",                # 设置音频为单声道
    "-ar", "16000",            # 设置采样率为 16kHz
    "-y",                      # 如果文件已存在则覆盖
    audio_path       # 输出文件路径
]

# 运行 ffmpeg 命令
subprocess.run(command)

print(f"音频已提取并保存为 {audio_path}")

# 使用 pydub 加载音频并进行转换 这个库有问题，一直报错


# 加载 Vosk 模型
if not os.path.exists(model_path):
    print(f"模型路径 '{model_path}' 不存在，请下载模型并解压到该路径")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# 读取音频文件并进行语音识别
wf = wave.open(audio_path, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("请确保音频为 16kHz 采样率、单声道 WAV 格式")
    exit(1)

# 识别音频内容并将结果保存到列表中
results = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        results.append(result)

wf.close()

# 打开视频并逐帧处理
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
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
    for result in results:
        if 'result' not in result:
            continue
        start_time = result['result'][0]['start']
        end_time = result['result'][-1]['end']

        if start_time <= current_time <= end_time:
            current_text = result['text']
            break
        else:
            current_text = ""

    # 在当前帧上显示字幕
    if current_text:
        cv2.putText(frame, current_text, (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 写入处理后的帧
    out.write(frame)
    current_frame += 1

    # 显示视频帧（可选，用于调试）
    cv2.imshow('Video with Subtitles', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
os.remove(audio_path)

print(f"字幕已叠加并保存为 {output_video_path}")
