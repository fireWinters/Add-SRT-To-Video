'''
Author: Diana Tang
Date: 2024-10-17 20:05:38
LastEditors: Diana Tang
Description: some description
FilePath: /Add-SRT-To-Video/start.py
'''
from setuptools import setup, find_packages

setup(
    name="Add-SRT-To-Video",  # 项目名称
    version="1.0.0",  # 项目版本
    author="Diana Tang",  # 作者名
    author_email="your.email@example.com",  # 作者邮箱
    description="utomatically generate and embed subtitles into our videos",  # 项目简短描述
    long_description=open('README.md').read(),  # 长描述，通常是README内容
    long_description_content_type='text/markdown',  # 长描述的格式
    url="https://github.com/fireWinters/Add-SRT-To-Video",  # 项目主页
    packages=find_packages(),  # 自动找到项目中的所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # MIT 许可协议
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # 最低Python版本要求 need Python 3.7 or newer
    install_requires=[  # 项目依赖ffmpeg
       'openai-whisper',
    ],
    include_package_data=True,
)
