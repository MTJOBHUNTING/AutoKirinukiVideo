from autoedit.nvAudioEffects import *
from message.log import *
from autoedit.settings import S_NVAFX_MODELS_DIR_PATH
from pathlib import Path
from math import ceil, log10
from tqdm import tqdm

import audioop
import wave
import numpy as np

class NvAFX:
    def __init__(self, input_audio_path: Path, debug_flag: bool = False, sample_rate: int = 16000, model_file: str = 'denoiser_16k.trtpkg') -> None:
        self.handle = c_void_p(None) # エフェクトハンドル用
        self.num_samples_per_frame = c_uint(160) # フレームあたりのサンプル数
        self.num_channels = c_uint(1) # チャンネル数
        self.sample_rate = sample_rate # サンプルレート
        self.model_path = Path(S_NVAFX_MODELS_DIR_PATH, model_file) # 使用するモデルのパス
        self.debug_flag = debug_flag # デバッグモード
        self.volume_level_np: np.ndarray = None # 音量(dB)のnumpyリスト
        
        self.input_audio_path: Path = input_audio_path # ノイズ除去を行う音声ファイルパス

        # セットアップに使用する関数と引数のリスト
        self.setup_func_list = [
            {
                
                # エフェクトハンドルを作成する関数
                'function': NvAFX_CreateEffect,
                # 使用するエフェクトはノイズ除去で、エフェクトハンドルをself.handleに渡す。
                'args': (NVAFX_EFFECT_DENOISER, byref(self.handle)),
                'failed_check_flag': True
            },
            {
                # エフェクトハンドルに整数パラメータを与える関数
                'function': NvAFX_SetU32,
                # サンプルレート値を設定する。
                'args': (self.handle, NVAFX_PARAM_DENOISER_SAMPLE_RATE, self.sample_rate),
                'failed_check_flag': True
            },
            {
                # エフェクトハンドルに浮動小数点数パラメータを与える関数
                'function': NvAFX_SetFloat,
                # ノイズ除去の強度を設定する。
                'args': (self.handle, NVAFX_PARAM_DENOISER_INTENSITY_RATIO, 1.0),
                'failed_check_flag': True
            },
            {
                # エフェクトハンドルに文字列パラメータを与える関数
                'function': NvAFX_SetString,
                # ノイズ除去で使用するモデルの絶対パスを設定する。
                'args': (self.handle, NVAFX_PARAM_MODEL_PATH, str(self.model_path.absolute())),
                'failed_check_flag': True
            },
            {
                # エフェクトを読み込む関数
                'function': NvAFX_Load,
                # 読み込むエフェクトハンドルを指定する。
                'args': (self.handle, ),
                'failed_check_flag': True
            },
            {
                # エフェクトの整数パラメータを取得する関数
                'function': NvAFX_GetU32,
                # フレームあたりのサンプル数を取得
                'args': (self.handle, NVAFX_PARAM_NUM_SAMPLES_PER_FRAME, byref(self.num_samples_per_frame)),
                'failed_check_flag': False
            },
            {
                # エフェクトの整数パラメータを取得する関数
                'function': NvAFX_GetU32,
                # チャンネル数を取得
                'args': (self.handle, NVAFX_PARAM_DENOISER_NUM_CHANNELS, byref(self.num_channels)),
                'failed_check_flag': False
            }
        ]

    def setup_and_run(self) -> bool:
        """
        NvAFXのセットアップと実行を行う関数
        (
            成功: Trueを返す
            失敗: Falseを返す
        )
        """
        if self.debug_flag:
            print_log(EnumMessage.START_SETUP)

        # モデルファイルが存在しない場合は終了
        if not self.model_path.exists():
            if self.debug_flag:
                print_log(EnumMessage.NOT_EXISTS_MODEL_FILE, EnumLogType.ERROR)
            return False
        
        # セットアップするための関数を呼び出す
        for setup_func_dict in self.setup_func_list:
            setup_func, setup_args, failed_check_flag = setup_func_dict['function'], setup_func_dict['args'], setup_func_dict['failed_check_flag']

            status = setup_func(*setup_args)
            
            # 失敗確認フラグが有効であり、かつセットアップ中に、失敗した場合はメモリを解放して終了する
            if failed_check_flag and not self.free_memory_on_failed_status(status):
                return False

        # 入力された音声ファイルが存在しない場合は、メモリを解放して終了する
        if not self.input_audio_path.exists():
            self.run_free_memory()
            return False

        if self.debug_flag:
            print_log(EnumMessage.COMPLETE_SETUP)


        # 音声データを読み込む
        with wave.open(str(self.input_audio_path.absolute()), 'rb') as input_audio_data:
            # 音声データのサンプル幅(バイト数)
            input_audio_sample_width = input_audio_data.getsampwidth()

            # 音声ファイルに合わせたdtypeに設定
            audio_dtype: str = f'<i{input_audio_sample_width}'

            # 一時的にノイズ除去した音声データの一部を出力する配列
            output_audio_data_temp_segment_np = np.zeros(self.num_samples_per_frame.value, dtype=audio_dtype)
            output_audio_data_temp_segment_np = output_audio_data_temp_segment_np.astype(np.float32)
            # 上データのポインタ
            output_audio_data_temp_segment_c  = output_audio_data_temp_segment_np.ctypes.data_as(POINTER(c_float))

            # 音声データを -1 ～ +1 の範囲に正規化するために必要な値
            input_audio_data_normalize_value: float = 2 ** (input_audio_sample_width * 8) / 2

            # 音声データをすべてノイズ除去するために必要なループ数
            # (音声データの全フレーム数 / 一度にノイズ除去を行うフレーム数) を切り上げした数値がノイズ除去に必要なループ数になります
            num_denoise_loops: int = ceil(input_audio_data.getnframes() / self.num_samples_per_frame.value)

            # ノイズ除去を行うためのループ範囲
            loop_range = range(num_denoise_loops)

            if self.debug_flag:
                print_log(EnumMessage.START_DENOISE)

            # デバッグモードが有効の場合は、tqdmで表示
            if self.debug_flag:
                loop_range = tqdm(loop_range, desc=f'[{EnumLogType.DEFAULT.value}]: ')

            self.volume_level_np = np.zeros(num_denoise_loops)

            for i in loop_range:
                # 取得した音声データの一部(バイト型)
                input_audio_data_bytes_segment = input_audio_data.readframes(self.num_samples_per_frame.value)

                # 取得した音声データをNvAFXに読み込みが可能な状態にする
                input_audio_data_int_segment_np: np.ndarray = np.frombuffer(input_audio_data_bytes_segment, dtype=audio_dtype) / input_audio_data_normalize_value
                # データ数がnum_samples_per_frame未満の場合、末尾をゼロ埋めする。
                if input_audio_data_int_segment_np.size < self.num_samples_per_frame.value:
                    np_zeros = np.zeros(self.num_samples_per_frame.value - input_audio_data_int_segment_np.size, dtype=audio_dtype)
                    input_audio_data_int_segment_np = np.concatenate((input_audio_data_int_segment_np, np_zeros))

                input_audio_data_float_segment_np = input_audio_data_int_segment_np.astype(np.float32)
                input_audio_data_float_segment_c  = input_audio_data_float_segment_np.ctypes.data_as(POINTER(c_float))
                
                # ノイズ除去を実行する
                status = NvAFX_Run(self.handle, input_audio_data_float_segment_c, output_audio_data_temp_segment_c, self.num_samples_per_frame, self.num_channels.value)
                # ノイズ除去に失敗した場合はメモリを解放して終了
                if not self.free_memory_on_failed_status(status):
                    return False

                # audioop にとって扱いやすいデータに変換
                _audio_data_int16_np = output_audio_data_temp_segment_np * input_audio_data_normalize_value
                _audio_data_int16_np = _audio_data_int16_np.astype(dtype=audio_dtype)
                _audio_data_int16_bytes = _audio_data_int16_np.tobytes()

                # 一部のノイズ除去データから音量(dB)を取得
                volume_level = self.get_volume_level_from_denoise_audio_data(_audio_data_int16_bytes, input_audio_sample_width, input_audio_data_normalize_value)

                # 音量データを保存する
                self.volume_level_np[i] = volume_level
            
            if self.debug_flag:
                print_log(EnumMessage.COMPLETE_DENOISE)
                
            # メモリ解放
            self.run_free_memory()

        return True
    
    def get_volume_level_from_denoise_audio_data(self, data: bytes, width: int, normalize_value: float) -> float:
        """ ノイズ除去データから音量(dB)を取得する関数 """
        # RMSを取得し、正規化
        rms = audioop.rms(data, width) / normalize_value
        # RMSが0以下の場合はエラー対策のため、想定される音量最低値を計算する
        if rms <= 0:
            rms = 1 / normalize_value
        
        return self.get_volume_level_from_rms(rms)

    def get_volume_level_from_rms(self, rms: float) -> float:
        """ RMSから音量(dB)を計算し、取得する関数 """
        return 20 * log10(rms)

    def free_memory_on_failed_status(self, current_status: int) -> bool:
        """
        ステータスが失敗の場合、メモリを解放する関数
        (
            ステータスが成功: Trueを返す
            ステータスが失敗: メモリを解放し、Falseを返す
        )
        """

        # 現在のステータスが成功状態の場合は何もせず終了
        if current_status == NVAFX_STATUS_SUCCESS:
            return True
        
        if self.debug_flag:
            print_log(EnumMessage.FREE_MEMORY_ON_FAILED_STATUS, EnumLogType.ERROR)

        # メモリ解放
        self.run_free_memory()

        return False
    
    def run_free_memory(self):
        """ メモリを解放を実行する関数 """

        # handle値が設定されてる場合はメモリを解放する。
        if self.handle.value is not None:
            self.destroy_handle()

    def destroy_handle(self):
        """ エフェクトハンドルを解放する関数 """
        NvAFX_DestroyEffect(self.handle)