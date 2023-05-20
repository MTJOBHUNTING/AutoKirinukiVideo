from enum import Enum
from typing import List, Any

class EnumLogType(Enum):
    DEFAULT: str = 'ログ'
    ERROR: str = 'エラー'

class EnumMessage(Enum):
    NVAFX_START_SETUP: str = 'セットアップ中...'
    NVAFX_COMPLETE_SETUP: str = 'セットアップが完了しました！'
    NVAFX_START_DENOISE: str = 'ノイズを除去中...'
    NVAFX_COMPLETE_DENOISE: str = 'ノイズ除去が完了しました！'
    NVAFX_NOT_EXISTS_MODEL_FILE: str = 'モデルファイルが存在しません。'
    NVAFX_FREE_MEMORY_ON_FAILED_STATUS: str = '失敗時のステータスです。メモリを解放します。'

    API_DETECT_MODE_VIEW: str = '検出モード: {}'

def print_log(message: EnumMessage, log_type: EnumLogType = EnumLogType.DEFAULT, format_list: List[Any] = list()) -> None:
    """ ログを表示するための関数 """
    print(f'{get_log_prefix(log_type)}{message.value.format(*format_list)}')

def get_log_prefix(log_type: EnumLogType = EnumLogType.DEFAULT):
    return f'[{log_type.value}]: '