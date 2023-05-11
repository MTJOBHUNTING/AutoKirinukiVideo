from enum import Enum

class EnumHTML(Enum):
    MAIN: str = 'index.html' # メイン画面
    
class EnumCSS(Enum):
    MAIN: str = 'style.css' # メインスタイル
    BOOTSTRAP: str = 'bootstrap.min.css'

class EnumJS(Enum):
    MAIN: str = 'script.js' # メインスクリプト
    BOOTSTRAP: str = 'bootstrap.bundle.min.js'