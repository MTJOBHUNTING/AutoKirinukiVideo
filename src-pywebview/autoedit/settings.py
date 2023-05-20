from pathlib import Path

import os

# NvAFXのフォルダのパス
S_NVAFX_DIR_PATH = Path(os.environ['ProgramW6432'], 'NVIDIA Corporation', 'NVIDIA Audio Effects SDK')
# NvAFXのモデルフォルダのパス
S_NVAFX_MODELS_DIR_PATH = Path(S_NVAFX_DIR_PATH, 'models')
