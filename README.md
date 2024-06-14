# Video Editor System

#### 使用技術
<p style="display: inline">
<img src="https://img.shields.io/badge/-Linux-212121.svg?logo=linux&style=popout">
<img src="https://img.shields.io/badge/-Python-FFC107.svg?logo=python&style=popout">
<img src="https://img.shields.io/badge/-FFmpeg-007808.svg?logo=ffmpeg&style=popout">
</p>

&nbsp;

## 概要

Video Editor System はMP4ファイルから圧縮，解像度・アスペクト比の調整，音声変換，GIFを生成するプログラムです．
このプログラムでは，FFMPEGライブラリを用いてタスクを実行し，品質と互換性を確保しています．

&nbsp;

#### 操作方法

1. ターミナルを開きserver.pyを立ち上げる<br>
```bash
$ python server.py
```

2. 別のターミナルを開きclient.pyを立ち上げる<br>
```bash
$ python client.py
```

3. './data'内のMP4ファイルの一覧が表示されるので変換したいMP4ファイルに該当する数字を入力してください．<br>
```bash
./data/sample.mp4 → 1

Select the data number you want to send to the server from above. 
→ 1
```

4. 選択したMP4ファイルでよければ y と入力してください．<br>
```bash
Are you sure it is sample.mp4? (y/n) → y
Selected file bytes: 3.52MB
```

5. どのように変換したいか尋ねてくるので該当する数字を入力してください．<br>
```bash
1: compress
2: change_resolution
3: change_aspect_ratio
4: convert_to_audio
5: convert_to_gif

Please enter a number. → 1
The transmission of the header has been completed.

sending...
Transmission of MP4 file completed!
Recived output_header!
```

6. 以下が表示されれば './output' 内に変換されたファイルが保存されます．<br>
```bash
Recived sample_compress.mp4
```

&nbsp;

## ディレクトリ構成
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
#### 開発環境
| OS・言語・ライブラリ | バージョン |
| :------- | :------ |
| Ubuntu | 22.04.4 LTS |
| Python | 3.10.12 |
| ffmpeg | 4.4.2 |
<br>

#### ffmpegのインストール手順
**Ubuntu**<br>
Ubuntuにffmpegをインストール
```bash
$ sudo apt update
$ sudo apt install ffmpeg

ffmpegのインストール確認
$ ffmpeg -version

ffmpeg-pythonライブラリのインストール
$ pip install ffmpeg-python
```

&nbsp;