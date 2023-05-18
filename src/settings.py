from typing import Set

# デバッグモード
S_DEBUG_FLAG: bool = True

""" アプリの仕様 """
# タイトル
S_APP_TITLE: str = '自動動画編集ソフト'
# デフォルト幅
S_APP_WIDTH: int = 1280
# デフォルト高さ
S_APP_HEIGHT: int = 720
# 使用するウェブエンジン
S_APP_WEB_ENGINE: str = 'edgechromium'

""" ファイルの出力先 """
# プロジェクトファイルの出力先
S_PROJECT_FILE_OUTPUT: str = './output/'

""" アプリのGUI系ファイルが保存されたディレクトリの名前やパス """
# GUIフォルダの相対パス
S_GUI_DIR_PATH: str = './gui/'
# HTMLフォルダの名前
S_GUI_HTML_DIR_NAME: str = 'html'
# CSSフォルダの名前
S_GUI_CSS_DIR_NAME: str = 'css'
# JavaScriptフォルダの名前
S_GUI_JS_DIR_NAME: str = 'js'

# アプリ内のデフォルトエンコーディング
S_DEFAULT_ENCODING: str = 'UTF-8'

""" ファイル読み込みのダイアログ系 """
# 動画ファイルのタイプ名
S_FILE_TYPE_VIDEO_NAME: str = '動画ファイル'
# 読み込み可能な動画ファイルの拡張子の集合
S_VIDEO_FILE_EXTENSION_SET: Set[str] = {
    'avi',
    'mp4'
}

""" ノイズ除去時に使用する音声データのパラメータ """
# サンプルレート
S_DENOISE_SAMPLE_RATE: int = 16000
# チャンネル数
S_DENOISE_CHANNELS: int = 1

""" ffmpeg系 """
# ffmpeg.exe のあるパス
S_FFMPEG_EXE_PATH: str  = 'ffmpeg'
# ffprobe.exe のあるパス
S_FFPROBE_EXE_PATH: str = 'ffprobe'
# ffmpegで動画ファイルから音声ファイルに変換する時の引数辞書
S_FFMPEG_ARGS_VIDEO_TO_AUDIO: dict = {
    'vn': None, # 動画無効化
    'y': None, # 上書き許可
    'ar': S_DENOISE_SAMPLE_RATE, # サンプルレート指定
    'ac': S_DENOISE_CHANNELS # チャンネル数指定
}

""" 一時ファイル系 """
# 一時フォルダの相対パス
S_TEMP_DIR_PATH: str = './temp/'
# 一時入力ファイルを保存するフォルダ名
S_TEMP_INPUT_DIR_NAME: str = 'input'
# 一時出力ファイルを保存するフォルダ名
S_TEMP_OUTPUT_DIR_NAME: str = 'output'

""" ジャンプカットするために必要なしきい値(音量モード) """
# 指定した値以上であれば、声として認識する音量(パーセント)
S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD:  float = 0.4
# 指定した値以下であれば、雑音として認識する音量(パーセント)
S_CLOSE_VOICE_VOLUME_LEVEL_THRESHOLD: float = 0.3
# 何秒間 S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD の値以上であれば、声として認識するのか
S_OPEN_VOICE_VOLUME_LEVEL_TIME:  float = 0.15
# 何秒間 S_CLOSE_VOICE_VOLUME_LEVEL_THRESHOLD の値以下であれば、雑音として認識するのか
S_CLOSE_VOICE_VOLUME_LEVEL_TIME: float = 0.15

""" ジャンプカットするために必要なしきい値(波形モード) """
# 指定した値以上であれば、声として認識する波形値
S_VOICE_DETECT_THRESHOLD_WAVEFORM:   float = 0.05
# 一瞬だけ無音と検出されないために、指定した秒数は無視する
S_VOICE_DETECT_IGNORE_SILENCE_TIME_WAVEFORM: float = 0.3
# 一瞬だけ声と検出されないために、指定した秒数は無視する
S_VOICE_DETECT_IGNORE_VOICE_TIME_WAVEFORM: float = 0.15
# ノイズ発生を最小限にするため、カットするタイミングから余分に声と判定させる秒数 (以下の値の秒数 x 2 = 余分に声と判定させる秒数)
S_VOICE_DETECT_EXTRA_TIME_WAVEFORM: float = 0.1