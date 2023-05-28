import webview
from webview import Window
from pathlib import Path
from utils import make_dir_need_dirs, get_dir_all_file_pathes
from api import API
from settings import *

class WebViewWindow:
    def __init__(self) -> None:
        self.api: API = API()
        self.window: Window = webview.create_window(S_APP_TITLE, js_api=self.api, width=S_APP_WIDTH, height=S_APP_HEIGHT, frameless=True)
        self.api.window: Window = self.window

    def run(self):
        """ アプリを開く """
        webview.start(self.thread_func, gui=S_APP_WEB_ENGINE, debug=S_DEBUG_FLAG)

    def thread_func(self):
        # GUI関連のファイルが存在するディレクトリパス
        gui_dir_path = Path(S_GUI_DIR_PATH)
        # GUIディレクトリに存在するすべての関連ファイルを取得
        gui_dir_all_file_pathes = get_dir_all_file_pathes(gui_dir_path)

        # htmlファイルを一番最初に読み込むためにソートを行う
        gui_dir_all_file_pathes.sort(key=lambda x: x.suffix == '.html', reverse=True)
        
        # GUI関連ファイルをすべて読み込む
        for gui_file_path in gui_dir_all_file_pathes:
            self.load_gui_data(gui_file_path)
                
    def load_gui_data(self, gui_file_path: Path):
        """ GUI関連のファイルパス(HTML, JavaScript, CSS)を指定し、WebViewWindowに読み込む関数 """
        # 指定したファイルのデータをテキストとして取得
        _gui_data_text: str = gui_file_path.read_text(encoding=S_DEFAULT_ENCODING)
        # 指定したファイルの拡張子
        file_extension: str = gui_file_path.suffix

        # HTMLファイルの場合
        if file_extension == '.html':
            self.window.load_html(_gui_data_text)
        # JavaScriptファイルの場合
        elif file_extension == '.js':
            self.window.evaluate_js(_gui_data_text)
        # CSSファイルの場合
        elif file_extension == '.css':
            self.window.load_css(_gui_data_text)

def main():
    """ メイン関数 """
    # フォルダの存在確認と作成
    make_dir_need_dirs()
    main_window = WebViewWindow()
    main_window.run() # ウィンドウを開く

if __name__ == '__main__':
    main()