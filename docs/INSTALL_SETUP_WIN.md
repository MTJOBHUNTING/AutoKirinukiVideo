# 開発環境のセットアップ(Windows)
## 前提について
まず、ここでの説明については、Windows環境での実行を想定しています。

また、以下のインストールと、環境変数の設定は済んでいる状態を前提とした説明になります。
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
次に、クローンしたレポジトリのディレクトリに移動します。
```
cd AutoKirinukiVideo
```
次に、Node.jsパッケージのインストールを行います。
```
npm ci
```
最後に、ビルドを行います。
```
npm run build
```
## アプリの実行まで
まず、仮想環境を作成します。
```
python -m venv venv
```
次に、仮想環境を有効化します。
```
.\venv\Scripts\activate
```
次に、Pythonパッケージのインストールを行います。
```
pip install -r requirements.txt
```
最後に、アプリを実行します。
```
python .\src-pywebview\main.py 
```