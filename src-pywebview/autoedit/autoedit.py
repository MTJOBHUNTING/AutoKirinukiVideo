from autoedit.mode import DetectMode
from pathlib import Path
from settings import *
from typing import List, Optional
from enum import Enum
import numpy as np

class ArrayPos(Enum):
    LEFT: int = 0
    RIGHT: int = 1
    
class AutoEdit:
    def __init__(self, video_fps: int, input_video_path: Path, voice_detect_need_data_np: np.ndarray, sample_rate: int, num_samples_per_frame: int) -> None:
        self.video_fps = video_fps # 動画ファイルのFPS
        self.audio_fps = num_samples_per_frame / sample_rate # 音声ファイルのFPS
        self.input_video_path = input_video_path # 動画ファイルのパス
        self.voice_detect_need_data_np = voice_detect_need_data_np # 声を発した部分を判定するために必要なデータのnumpyリスト
        self.sample_rate = sample_rate # サンプルレート
        self.num_samples_per_frame = num_samples_per_frame # フレームあたりのサンプル数

    def replace_consecutive_data(self, target_voice_detect_need_data_np: np.ndarray, consecutive_from_data_secs_border: float, from_data: int, to_data: int) -> None:
        """
        NumPyリストの中に指定された秒数の間、「from_data」が続いていた場合、「to_data」へ置き換える関数 

        引数:
            target_voice_detect_need_data_np: 対象データ
            consecutive_from_data_secs_border: 指定された秒数
            from_data: 置き換え前のデータ
            to_data: 置き換え後のデータ
        """
        start_ix: int = -1 # 初期化
        for current_ix, current_data in enumerate(target_voice_detect_need_data_np):
            # 現在のデータが変換対象のデータの場合はcontinueする。ただし、開始インデックス番号が指定されてない場合は現在の番号を指定
            if current_data == from_data:
                if start_ix == -1:
                    start_ix = current_ix
                continue
            # 変換対象のデータが何秒間続いたのか
            consecutive_from_data_secs: int = (current_ix - start_ix + 1) * self.audio_fps
            # 開始インデックス番号が指定されており、変換対象データが引数で指定された秒数以内であれば変換を行う。
            if start_ix != -1:
                if consecutive_from_data_secs < consecutive_from_data_secs_border:
                    target_voice_detect_need_data_np[start_ix:current_ix + 1] = to_data
                start_ix = -1 # 初期化


    def set_consecutive_data_by_pos(self, target_data_np: np.ndarray, target_data: int, replace_data: int, array_pos: ArrayPos):
        """ 指定した配列に target_data が連続していた場合、一番右、もしくは左を残す関数 
        replace_data は連続してた不要なデータを置き換えるときの状態の値
        """
        # ループで使用する、「前回のデータ」を初期化
        previous_data = replace_data

        # 左だけ残す場合は配列を反転させる
        if array_pos == ArrayPos.LEFT:
            target_data_np = target_data_np[::-1]

        # 最後のデータを一時的に保存
        temp_last_data: int = target_data_np[-1]

        # 配列に target_data が連続してた場合は 一番右だけ 残す。
        for current_ix, current_data in enumerate(target_data_np):
            if current_data == target_data:
                target_data_np[current_ix] = replace_data
            elif previous_data != current_data:
                target_data_np[current_ix - 1] = target_data

            # 前回のデータを更新
            previous_data = current_data

        # 最後のデータが target_data だった時のために、一時的に保存したデータに上書き
        if temp_last_data == target_data:
            target_data_np[-1] = temp_last_data

        # 左だけ残す場合はもう一度配列を反転させることで完成する
        if array_pos == ArrayPos.LEFT:
            target_data_np = target_data_np[::-1]
            

    def set_extra_voice_data(self, target_voice_detect_need_data_np: np.ndarray, extra_time_secs: float) -> None:
        """ ノイズ発生を最小限にするため、余分に声と判断させる """
        # ループで使用する、「前回のデータ」を初期化
        previous_data = 0
        # ループ時にバグらせないために、コピーしておく
        _target_voice_detect_need_data_np_copied = target_voice_detect_need_data_np.copy()

        # 何データ分、余分に声と判断させるか
        len_extra_data: int = int(extra_time_secs / self.audio_fps)

        # 対象データの数
        len_target_data = len(target_voice_detect_need_data_np)

        for current_ix, current_data in enumerate(_target_voice_detect_need_data_np_copied):
            # 現在のデータと前回のデータが一致した場合、continue
            if current_data == previous_data:
                continue

            # 現在のデータが、声を発した部分だった場合、現在の添え字から len_extra_data 分、後ろを余分に声と判定させる
            if current_data == 1:
                if current_ix - len_extra_data >= 0:
                    target_voice_detect_need_data_np[current_ix - len_extra_data:current_ix] = 1
                else:
                    target_voice_detect_need_data_np[:current_ix] = 1
            # 現在のデータが、無音部分だった場合、現在の添え字から len_extra_data 分、先を余分に声と判定させる
            else:
                if current_ix + len_extra_data < len_target_data:
                    target_voice_detect_need_data_np[current_ix:current_ix + len_extra_data] = 1
                else:
                    target_voice_detect_need_data_np[current_ix:] = 1
                
            # 前回のデータを更新
            previous_data = current_data
        
    def get_voice_time_range_list(self, detect_mode: DetectMode) -> List[List[int]]:
        """ 声を発した範囲を取得する関数 """
        # 声を発した範囲を取得するために扱いやすくしたデータ
        detect_data: Optional[np.ndarray] = None
        # 音量データから検出する
        if detect_mode == DetectMode.VOLUME:
            # 全体の中で最も低い音量(dB)を取得(絶対値)
            min_volume_level = abs(np.min(self.voice_detect_need_data_np))
            # 正規化を行う(0 ~ 1までのデータになる)
            voice_detect_need_data_np_normalized: np.ndarray = 1 + self.voice_detect_need_data_np / min_volume_level
            voice_detect_need_data_np_normalized /= np.max(voice_detect_need_data_np_normalized)
            
            # S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD 以上の値は声を発した部分とし、1と0だけのデータへ変換する([True, False] => [1, 0])
            voiced_data_np = (voice_detect_need_data_np_normalized >= S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD).astype(np.uint)
            # S_OPEN_VOICE_VOLUME_LEVEL_TIME 秒間 S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD 以上の音量だった場合は声と判定する
            self.replace_consecutive_data(voiced_data_np, S_OPEN_VOICE_VOLUME_LEVEL_TIME, 1, 0)
            # 声を発した最初の部分が配列の何番目かを分かるように、連続した声を発した部分の一番左側だけ残す
            self.set_consecutive_data_by_pos(voiced_data_np, 1, 0, ArrayPos.LEFT)
            # S_CLOSE_VOICE_VOLUME_LEVEL_THRESHOLD 以下の値は無音部分とし、-1と0だけのデータへ変換する([True, False] => [-1, 0])
            silenced_data_np = (voice_detect_need_data_np_normalized <= S_CLOSE_VOICE_VOLUME_LEVEL_THRESHOLD).astype(np.uint) * -1
            # S_CLOSE_VOICE_VOLUME_LEVEL_TIME 秒間 S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD 以下の音量だった場合は無音と判定する
            self.replace_consecutive_data(silenced_data_np, S_CLOSE_VOICE_VOLUME_LEVEL_TIME, -1, 0)
            # 無音になった最後の部分が配列の何番目かを分かるように、連続した無音部分の一番左側だけ残す
            self.set_consecutive_data_by_pos(silenced_data_np, -1, 0, ArrayPos.LEFT)

            # 声を発した範囲を取得するために扱いやすいよう、二つのデータを結合する
            detect_data = voiced_data_np + silenced_data_np

        # 波形データから検出する
        elif detect_mode == DetectMode.WAVEFORM:
            # 正規化するために最大値をとる
            _max = max(self.voice_detect_need_data_np)
            # 正規化を行う(0 ~ 1までのデータになる)
            voice_detect_need_data_np_normalized = self.voice_detect_need_data_np / _max
            # S_OPEN_VOICE_VOLUME_LEVEL_THRESHOLD_WAVEFORM 以上の値は声を発した部分とし、1と0だけのデータへ変換する([True, False] => [1, 0])
            voice_detect_need_data_np_normalized = (voice_detect_need_data_np_normalized >= S_VOICE_DETECT_THRESHOLD_WAVEFORM).astype(np.uint)
            # S_VOICE_DETECT_IGNORE_TIME_WAVEFORM 秒以内の無音であれば、声と認識させる
            self.replace_consecutive_data(voice_detect_need_data_np_normalized, S_VOICE_DETECT_IGNORE_SILENCE_TIME_WAVEFORM, 0, 1)
            # S_VOICE_DETECT_IGNORE_VOICE_TIME_WAVEFORM 秒以内の声であれば、無音と認識させる
            self.replace_consecutive_data(voice_detect_need_data_np_normalized, S_VOICE_DETECT_IGNORE_VOICE_TIME_WAVEFORM, 1, 0)
            # 基準をもとにカットすることでノイズが発生してしまうため、カットするタイミングから S_VOICE_DETECT_EXTRA_TIME_WAVEFORM 秒間は余分に声と判定させる
            self.set_extra_voice_data(voice_detect_need_data_np_normalized, S_VOICE_DETECT_EXTRA_TIME_WAVEFORM)

            # 声を発した範囲を取得するために扱いやすいよう、データを二つに分割し、結合する
            voiced_data_np = voice_detect_need_data_np_normalized.copy()
            silenced_data_np = voice_detect_need_data_np_normalized.copy() * -1 # 無音と判定するために -1 へ
            
            self.set_consecutive_data_by_pos(voiced_data_np, 1, 0, ArrayPos.LEFT)
            self.set_consecutive_data_by_pos(silenced_data_np, -1, 0, ArrayPos.RIGHT)

            detect_data = voiced_data_np + silenced_data_np
            
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

        """
        current_data に入る値は、 (1, -1, 0) のどれかです。
        1: 声を発したタイミング
        -1: 無音となるタイミング
        0: 何もしない
        """
        # ループで使用する、「前回のデータ」を初期化(初期値は無音とする)
        previous_data = -1
        for current_ix, current_data in enumerate(detect_data):
            # 現在のデータが、無視しても良いデータ、もしくは前回のデータと一致した場合は、continue
            if current_data in (0, previous_data):
                continue
            # 現在のフレーム数から秒数へ変換する
            current_seconds = current_ix * self.audio_fps
            # 声を発したタイミングであれば、
            if current_data == 1:
                voice_time_range_data.append(
                    # [開始時間, 終了時間]
                    [current_seconds, -1]
                )
            # 無音となるタイミングであれば、
            else:
                voice_time_range_data[-1][1] = current_seconds

            # 前回のデータを更新
            previous_data = current_data
                
        return voice_time_range_data
    