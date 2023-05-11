from pathlib import Path
from settings import *
from typing import List
import numpy as np

class AutoEdit:
    def __init__(self, video_fps: int, input_video_path: Path, volume_level_np: np.ndarray, sample_rate: int, num_samples_per_frame: int) -> None:
        self.video_fps = video_fps # 動画ファイルのFPS
        self.audio_fps = num_samples_per_frame / sample_rate # 音声ファイルのFPS
        self.input_video_path = input_video_path # 動画ファイルのパス
        self.volume_level_np = volume_level_np # 音量(dB)のnumpyリスト
        self.sample_rate = sample_rate # サンプルレート
        self.num_samples_per_frame = num_samples_per_frame # フレームあたりのサンプル数


    def get_voice_time_range_list(self) -> List[List[int]]:
        """ 声を発した範囲を取得する関数 """
        # 全体の中で最も低い音量(dB)を取得(絶対値)
        min_volume_level = abs(np.min(self.volume_level_np))
        # 音量の値ではなくパーセントで扱う
        volume_level_np_percent: np.ndarray = 1 + self.volume_level_np / min_volume_level
        volume_level_np_percent /= np.max(volume_level_np_percent)
        # 現在 OPEN 中か
        is_open_flag = False
        # 一時的な時間を保存しておくための変数
        temp_time = -1

        """
        最終的に出力する声を発した範囲のリストデータ
        
        例として以下のようなデータが入る
        DATA[?][0]: (声を発したタイミング)
        DATA[?][1]: (声が途切れたタイミング、ただし -1 は音声データの最後までという意味)
        DATA = [
            [1.2, 3.2],
            [5.6, 10.2],
            [20.2, -1]
        ]
        """
        voice_time_range_data: List[List[int]] = []

        for frame_ix, voice_level_percent in enumerate(volume_level_np_percent):
            # 現在のフレーム数から秒数へ変換する
            current_seconds = frame_ix * self.audio_fps
            # OPEN 状態であれば
            if is_open_flag:
                # 雑音として認識する音量(パーセント)より大きければ continue
                if voice_level_percent > S_CLOSE_VOICE_VOLUME_LEVEL_THRESHOLD:
                    temp_time = -1 # 雑音でないため、初期化
                    continue
                # CLOSE に必要な時間に達したら、終了状態にする。
                if temp_time >= 0 and current_seconds - temp_time >= S_CLOSE_VOICE_VOLUME_LEVEL_TIME:
                    # 終了時間を設定
                    voice_time_range_data[-1][1] = temp_time
                    is_open_flag = False
                    temp_time = -1 # 状態が変わるため、初期化
            # CLOSE 状態であれば
            else:
                # 声として認識する音量(パーセント)未満であれば continue
                if voice_level_percent < S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD:
                    temp_time = -1 # 雑音でないため、初期化
                    continue
                # OPEN に必要な時間に達したら、開始状態にする。
                if temp_time >= 0 and current_seconds - temp_time >= S_OPEN_VOICE_VOLUME_LEVEL_TIME:
                    # 声の発したタイミングのデータを追加
                    voice_time_range_data.append(
                        # [開始時間, 終了時間]
                        [temp_time, -1]
                    )
                    is_open_flag = True
                    temp_time = -1 # 状態が変わるため、初期化

            # continue されない。つまり(声 or 雑音)として認識した場合は、一時的な(開始 or 終了)時間として記録しておく
            if temp_time < 0:
                temp_time = current_seconds

        return voice_time_range_data

    def export_aviutl_exo_file():
        pass
