from webview import Window, OPEN_DIALOG
from settings import *
from typing import Tuple, Optional
from utils import get_file_types
from pathlib import Path
from message.log import *
from autoedit.mode import DetectMode
from autoedit.nvafx import NvAFX
from autoedit.autoedit import AutoEdit
from autoedit.extract_project import AviUtlFile, VideoData

import ffmpeg

class API:
    def __init__(self):
        self.window: Window = None

    def minimize_window(self):
        """ ウィンドウを最小化する関数 """
        self.window.minimize()

    def close_window(self):
        """ ウィンドウを閉じる関数 """
        self.window.destroy()

    def load_video(self, target_detect_mode_str: str):
        """ 動画ファイルを読み込み、ジャンプカットを行う。 """
        # 検出モード(文字列) => 検出モード(DetectMode)へ
        target_detect_mode: Optional[DetectMode] = DetectMode.fromStr(target_detect_mode_str)
        # 未知の検出モードだった場合は、何もせず終了する。
        if target_detect_mode is None:
            return

        # 選択してる検出モードの表示(デバッグが有効の場合)
        if S_DEBUG_FLAG:
            print_log(EnumMessage.API_DETECT_MODE_VIEW, format_list=[target_detect_mode_str])

        # 読み込み可能なファイルタイプ
        file_types: str = get_file_types(S_FILE_TYPE_VIDEO_NAME, S_VIDEO_FILE_EXTENSION_SET)

        # 動画ファイルを読み込むために、ダイアログを表示する
        file_abs_pathes: Tuple[str, ...] = self.window.create_file_dialog(OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        
        # ファイルが選択されなかった場合は、何もせず終了する。
        if file_abs_pathes is None:
            return
        
        # 選択されたファイルのパスを取得
        file_path: Path = Path(file_abs_pathes[0])

        # 選択されたファイルが、動画ファイルではない場合、何もせず終了する。
        # [1:] の説明: suffix で取得した拡張子は . も含まれるため、 . 部分を含めないために file_path.suffix[1:] で判定しています。
        if file_path.suffix[1:] not in S_VIDEO_FILE_EXTENSION_SET:
            return

        # 一時音声ファイルのパス
        temp_audio_file_path = Path(S_TEMP_DIR_PATH, S_TEMP_INPUT_DIR_NAME, f'{file_path.stem}.wav')

        # 動画ファイル -> 音声ファイル へ変換する。
        stream = ffmpeg.input(str(file_path.absolute()))
        stream = ffmpeg.output(stream, str(temp_audio_file_path.absolute()), **S_FFMPEG_ARGS_VIDEO_TO_AUDIO)
        ffmpeg.run(stream, cmd=S_FFMPEG_EXE_PATH, quiet=(not S_DEBUG_FLAG)) # quietを指定することで、ログのオンオフ切り替えを行う。

        # ノイズ除去
        nvafx = NvAFX(temp_audio_file_path, debug_flag=S_DEBUG_FLAG, sample_rate=S_DENOISE_SAMPLE_RATE)
        nvafx_success_flag = nvafx.setup_and_run(target_detect_mode) # セットアップとノイズ除去の実行
        
        # ノイズ除去に失敗した場合は終了する
        if not nvafx_success_flag:
            return
        
        # 動画ファイルからビデオデータインスタンスに変換する
        video_data = VideoData.from_path(file_path)

        # 自動動画編集を開始
        autoedit = AutoEdit(int(video_data.get_fps()), file_path, nvafx.voice_detect_need_data_np, nvafx.sample_rate, nvafx.num_samples_per_frame.value)
        # 声を発した部分をリスト化する
        voice_time_range_list = autoedit.get_voice_time_range_list(target_detect_mode)

        # AviUtlのプロジェクトファイルとして保存する。
        aviutl_file = AviUtlFile(file_path, voice_time_range_list, video_data)
        aviutl_file.extract(Path(S_PROJECT_FILE_OUTPUT, f'{file_path.stem}.exo'))