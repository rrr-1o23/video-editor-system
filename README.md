# Video Editor System

#### 使用技術
---
<img src="https://img.shields.io/badge/-Linux-212121.svg?logo=linux&style=popout">
<img src="https://img.shields.io/badge/-Python-FFC107.svg?logo=python&style=popout">
<img src="https://img.shields.io/badge/-FFmpeg-007808.svg?logo=ffmpeg&style=popout">

&nbsp;

## 概要
---
Video Editor System はMP4ファイルから圧縮，解像度・アスペクト比の調整，音声変換，GIFを生成するプログラムです．このプログラムでは，FFMPEGライブラリを用いてタスクを実行し，品質と互換性を確保しています．

&nbsp;

## ディレクトリ構成
---
```
.
├── server.py
├── client.py
├── data
│   └── sample.mp4
├── output
│   └── sample_compress.mp4
└── temp
```

&nbsp;

## 環境構築
---
#### 開発環境
| OS・言語・ライブラリ | バージョン |
| :------- | :------ |
| Ubuntu | 22.04.4 LTS |
| Python | 3.10.12 |
| ffmpeg | 4.4.2 |
<br>

#### ffmpegのインストール手順
---

**Ubuntu**
```bash
Ubuntuにffmpegをインストール
$ sudo apt update
$ sudo apt install ffmpeg

ffmpegのインストール確認
$ ffmpeg -version

ffmpeg-pythonライブラリのインストール
$ pip install ffmpeg-python
```
