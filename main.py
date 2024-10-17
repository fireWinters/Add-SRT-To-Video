'''
Author: Diana Tang
Date: 2024-10-17 22:11:41
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/main.py
'''
import os
import subprocess
import whisper

# 设置文件夹路径
videos_folder = "./videos"
output_folder = "./videos-subtitles"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取 videos 文件夹下的所有视频文件
video_files = [f for f in os.listdir(videos_folder) if f.endswith(('.mp4', '.avi', '.mkv'))]

# 加载 Whisper 模型
model = whisper.load_model("turbo")

# 处理每个视频文件
for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    audio_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}.wav")
    subtitle_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}.srt")
    final_output_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}_with_subtitles.mp4")

    # 提取视频中的音频并保存为 WAV 格式
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ac", "1",
        "-ar", "16000",
        "-y",
        audio_path
    ]
    subprocess.run(command)

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

    # 使用 ffmpeg 将原始音频和字幕叠加到最终输出视频中
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{subtitle_path}'",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        "-y",
        final_output_path
    ]

    subprocess.run(command)

    print(f"字幕已取得并保存为 {final_output_path}")
