from pathlib import Path
from typing import List, Optional
from settings import S_FFPROBE_EXE_PATH, S_DEFAULT_ENCODING

import ffmpeg

class VideoData:
    def __init__(self, video_width: int, video_height: int, video_rate: int, video_scale: int, video_len_frames: int, audio_sample_rate: int, audio_channels: int) -> None:
        self.video_width       = video_width        # 動画の幅
        self.video_height      = video_height       # 動画の高さ
        self.video_rate        = video_rate         # 動画のFPSの分子(60 / 1 = 60FPS)
        self.video_scale       = video_scale        # 動画のFPSの分母(60 / 1 = 60FPS)
        self.video_len_frames  = video_len_frames   # 動画の総フレーム数
        self.audio_sample_rate = audio_sample_rate  # 音声のサンプルレート
        self.audio_channels    = audio_channels     # 音声のチャンネル数
    
    def get_fps(self) -> float:
        """ 取得した情報からFPSを計算し返す関数 """
        return self.video_rate / self.video_scale

    @staticmethod
    def from_path(video_file_path: Path) -> Optional['VideoData']:
        """ 動画ファイルパスからVideoDataに変換する関数 """
        # ffprobe から動画情報を取得する
        probe = ffmpeg.probe(str(video_file_path.absolute()), cmd=S_FFPROBE_EXE_PATH)

        # 各変数の初期化
        video_width, video_height, video_rate, video_scale, video_len_frames = (None,) * 5
        audio_sample_rate, audio_channels = (None,) * 2

        # FPS は固定で60にしています。
        video_rate  = 60
        video_scale = 1

        for stream in probe['streams']:
            codec_type = stream['codec_type']

            # 動画の場合
            if codec_type == 'video':
                video_width = int(stream['width']) # 幅
                video_height = int(stream['height']) # 高さ
                video_len_frames = int(float(stream['duration']) * video_rate / video_scale)
            # 音声の場合
            elif codec_type == 'audio':
                audio_sample_rate = int(stream['sample_rate']) # サンプルレート
                audio_channels    = int(stream['channels']) # チャンネル数

        # 正常に動画情報が読み込めなかった場合はNoneを返す
        if None in (video_width, video_height, video_rate, video_scale, audio_sample_rate, audio_channels):
            return None

        # VideoDataを返す
        return VideoData(video_width, video_height, video_rate, video_scale, video_len_frames, audio_sample_rate, audio_channels)
        
class AviUtlFile:
    def __init__(self, video_file_path: Path, voice_time_range_data: List[List[int]], video_data: VideoData) -> None:
        self.video_file_path = video_file_path # 動画ファイルパス
        self.voice_time_range_data = voice_time_range_data # 声を発した範囲のリスト
        self.video_data = video_data # 動画情報の集まりであるクラス

        self.video_fps: float = video_data.get_fps()

        # 出力するファイルデータの中身を初期化
        self._data: List[str] = list()

        # 出力するファイルデータを更新
        self._update_data()

    def extract(self, project_file_path: Path):
        """ 指定したパスに、プロジェクトファイルを出力する関数 """

        # エンコーディングはShift_JISでないと、AviUtlに読み込むことができないので設定しています。
        with open(str(project_file_path.absolute()), "w", encoding='shift_jis') as f:
            f.write('\n'.join(self._data))


    def _get_video_data(self, i, current_frames, current_play_position, current_len_frames) -> List[str]:
        """ 指定された範囲のプロジェクトデータを返す(動画) """
        return [
            f'[{i}]',
            f'start={current_frames}',
            f'end={current_frames + current_len_frames}',
            'layer=1',
            f'group={1 + i * 2}',
            'overlay=1',
            'camera=0',
            f'[{i}.0]',
            '_name=動画ファイル',
            f'再生位置={current_play_position}',
            '再生速度=100.0',
            'ループ再生=0',
            'アルファチャンネルを読み込む=0',
            f'file={str(self.video_file_path.absolute())}',
            f'[{i}.1]',
            '_name=標準描画',
            'X=0.0',
            'Y=0.0',
            'Z=0.0',
            '拡大率=100.00',
            '透明度=0.0',
            '回転=0.00',
            'blend=0'
        ]
    def _get_audio_data(self, i, current_frames, current_len_frames, num_of_voice_time_range_datas) -> List[str]:
        """ 指定された範囲のプロジェクトデータを返す(音声) """
        return [
            f'[{i + num_of_voice_time_range_datas}]',
            f'start={current_frames}',
            f'end={current_frames + current_len_frames}',
            'layer=2',
            f'group={1 + i * 2}',
            'overlay=1',
            'audio=1',
            f'[{i + num_of_voice_time_range_datas}.0]',
            '_name=音声ファイル',
            '再生位置=0.00',
            '再生速度=100.0',
            'ループ再生=0',
            '動画ファイルと連携=1',
            f'file={str(self.video_file_path.absolute())}',
            f'[{i + num_of_voice_time_range_datas}.1]',
            '_name=標準再生',
            '音量=100.0',
            '左右=0.0'
        ]

    def _update_data(self):
        """ 出力するファイルデータを更新する関数 """
        # AviUtlプロジェクトファイルの最初に記述される動画情報をまとめたデータを初期値とする。
        self._data = [
            '[exedit]',
            f'width={self.video_data.video_width}',
            f'height={self.video_data.video_height}',
            f'rate={self.video_data.video_rate}',
            f'scale={self.video_data.video_scale}',
            f'length={self.video_data.video_len_frames}',
            f'audio_rate={self.video_data.audio_sample_rate}',
            f'audio_ch={self.video_data.audio_channels}'
        ]
        
        # AviUtlのプロジェクトファイルは、動画部分と音声部分で分かれているため、一時的にリストを作成する。
        _video_data, _audio_data = list(), list()
        # 切り抜く部分の動画データ数
        num_of_voice_time_range_datas = len(self.voice_time_range_data)
        # ループ時の現在フレーム数
        current_frames = 1

        for i, (start_time_secs, end_time_secs) in enumerate(self.voice_time_range_data):
            current_play_position = int(self.video_fps * start_time_secs) # 動画データ内部の再生位置
            current_len_frames = int(self.video_data.video_len_frames - self.video_fps * start_time_secs) # 切り抜く部分の動画データの長さ
            # 終了時間が -1 の場合は、「最後のフレームまで」という意味なので、切り抜く部分の動画データの長さを調整する
            if end_time_secs != -1:
                current_len_frames = int(self.video_fps * end_time_secs - self.video_fps * start_time_secs)

            _video_data += self._get_video_data(i, current_frames, current_play_position, current_len_frames) # 動画データを更新
            _audio_data += self._get_audio_data(i, current_frames, current_len_frames, num_of_voice_time_range_datas) # 音声データを更新

            # 動画の長さが伸びた分だけ、現在のフレーム数を更新する
            current_frames += current_len_frames + 1
        
        # 出力するファイルデータに動画データと音声データを追加する
        self._data += _video_data
        self._data += _audio_data