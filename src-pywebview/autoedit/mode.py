from enum import Enum
from typing import Optional

class DetectMode(Enum):
    """ 検出モード """
    VOLUME: str = 'VOLUME' # 音量から
    WAVEFORM: str = 'WAVEFORM' # 波形から

    @classmethod
    def fromStr(cls, target_str: str) -> Optional['DetectMode']:
        """ 文字列からDetectModeに変換 """

        # DetectModeの要素をすべて取得し、値と指定した文字列が一致したDetectModeを返す
        for detect_mode_item in DetectMode:
            if detect_mode_item.value != target_str:
                continue
            return detect_mode_item
        
        # 未知のDetectModeの場合はNoneを返す
        return None