from enum import Enum

class DetectMode(Enum):
    """ 検出モード """
    VOLUME: str = 'VOLUME' # 音量から
    WAVEFORM: str = 'WAVEFORM' # 波形から