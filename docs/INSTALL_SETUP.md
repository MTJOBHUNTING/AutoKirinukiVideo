# 開発環境のセットアップ
## 前提について
既に、以下のインストールと、環境変数の設定は済んでいる状態での説明になります。
- FFmpeg
- NVIDIA Audio Effects SDK
- Node.js
- Python
- Git
## 動作環境について
- Python 3.9.12
- Node.js 18.16.0
## GUIのビルドまで
まず、このレポジトリをクローンします。
```
git clone https://github.com/MTJOBHUNTING/AutoKirinukiVideo.git
```
次に、Nodeパッケージのインストールを行います。
```
npm ci
```
最後に、ビルドを行います。
```
npm run build
```
## アプリの実行まで
まず、Pythonパッケージのインストールを行います。
```
pip install -r requirements.txt
```
最後に、アプリを実行します。
```
python .\src-pywebview\main.py 
```