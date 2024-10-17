'''
Author: Diana Tang
Date: 2024-10-17 17:21:08
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/mp3tosrt.py
'''
from google.cloud import speech_v1p1beta1 as speech
import os

# 设置 Google Cloud 的 JSON 凭证
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

client = speech.SpeechClient()

# 配置音频文件信息
audio = speech.RecognitionAudio(uri="./1-1chinese.mp3")
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    language_code="en-US",
    enable_word_time_offsets=True,
)

# 开始转录
response = client.long_running_recognize(config=config, audio=audio)

for result in response.results:
    for word_info in result.alternatives[0].words:
        print(f"Word: {word_info.word}, start: {word_info.start_time.total_seconds()}, end: {word_info.end_time.total_seconds()}")
