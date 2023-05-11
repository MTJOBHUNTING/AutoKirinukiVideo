from enum import Enum

class EnumLogType(Enum):
    DEFAULT: str = 'ログ'
    ERROR: str = 'エラー'

class EnumMessage(Enum):
    START_SETUP: str = 'セットアップ中...'
    COMPLETE_SETUP: str = 'セットアップが完了しました！'
    START_DENOISE: str = 'ノイズを除去中...'
    COMPLETE_DENOISE: str = 'ノイズ除去が完了しました！'
    NOT_EXISTS_MODEL_FILE: str = 'モデルファイルが存在しません。'
    FREE_MEMORY_ON_FAILED_STATUS: str = '失敗時のステータスです。メモリを解放します。'

def print_log(message: EnumMessage, log_type: EnumLogType = EnumLogType.DEFAULT) -> None:
    """ ログを表示するための関数 """
    print(f'[{log_type.value}]: {message.value}')
