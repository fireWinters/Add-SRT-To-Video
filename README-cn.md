<!--
 * @Author: Diana Tang
 * @Date: 2024-10-17 20:31:30
 * @LastEditors: Diana Tang
 * @Description: some description
 * @FilePath: /Add-SRT-To-Video/README-cn.md
-->
### 自动为视频生成字幕

该项目使用 `ffmpeg` 和 [OpenAI 的 Whisper](https://openai.com/blog/whisper) 自动生成字幕并叠加到任何视频上。

## 安装

首先，你需要 Python 3.7 或更新版本。通过运行以下命令安装此项目：

```
pip install git+https://github.com/fireWinters/Add-SRT-To-Video.git
```

此外，你还需要安装 [`ffmpeg`](https://ffmpeg.org/)，它可以通过大多数包管理器进行安装：

- **在 Ubuntu 或 Debian 上**

  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

- **在 macOS 上使用 Homebrew 安装** (参考 https://brew.sh/)：

  ```bash
  brew install ffmpeg
  ```

- **在 Windows 上使用 Chocolatey 安装** (参考 https://chocolatey.org/)：

  ```bash
  choco install ffmpeg
  ```

## 使用说明

以下命令将生成一个 `subtitled/video.mp4` 文件，其中包含输入视频，并叠加了自动生成的字幕。

```
Add-SRT-To-Video /path/to/video.mp4 -o subtitled/
```

默认设置使用 `small` 模型，适合进行英文转录。你可以选择更大的模型来获得更好的效果（特别是对其他语言）。可用的模型包括：`tiny`、`tiny.en`、`base`、`base.en`、`small`、`small.en`、`medium`、`medium.en`、`large`。

```
Add-SRT-To-Video /path/to/video.mp4 --model medium
```

添加 `--task translate` 参数可以将字幕翻译成英文：

```
Add-SRT-To-Video /path/to/video.mp4 --task translate
```

运行以下命令查看所有可用选项：

```
Add-SRT-To-Video --help
```

## 许可协议

此脚本是开源的，并根据 MIT 许可证发布。详情请查看 [LICENSE](LICENSE) 文件。



## 用来压缩视频帧率的命令行语句
source source/main.sh
compress_video 20241019/input.mp4 20241019/output.mp4 23 medium 1280:720 30 128k