#!/bin/bash
###
 # @Author: Diana Tang
 # @Date: 2024-10-21 15:04:18
 # @LastEditors: Diana Tang
 # @Description: some description
 # @FilePath: /Add-SRT-To-Video/source/main.sh
### 

compress_video() {
    input_file="$1"
    output_file="$2"
    crf="${3:-23}"
    preset="${4:-medium}"
    scale="${5:-1280:720}"
    fps="${6:-30}"
    audio_bitrate="${7:-128k}"

    ffmpeg -i "$input_file" \
        -c:v libx265 -preset $preset -crf $crf \
        -vf "scale=$scale,fps=$fps" \
        -c:a aac -b:a $audio_bitrate \
        -movflags +faststart \
        "$output_file"
}

# 使用示例：
# compress_video input.mp4 output.mp4 23 medium 1280:720 30 128k

# 参数说明：
# $1: 输入文件
# $2: 输出文件
# $3: CRF值（0-51，默认23，越低质量越好）
# $4: 编码预设（ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow）
# $5: 输出分辨率（格式：宽:高，如 1280:720）
# $6: 输出帧率
# $7: 音频比特率