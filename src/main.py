import webview
from webview import Window
from pathlib import Path

from utils import make_dir_need_dirs
from gui import EnumHTML, EnumCSS, EnumJS
from api import API
from settings import *

class WebViewWindow:
    def __init__(self) -> None:
        self.api: API = API()
        self.window: Window = webview.create_window(S_APP_TITLE, js_api=self.api, width=S_APP_WIDTH, height=S_APP_HEIGHT)
        self.api.window: Window = self.window

    def thread_func(self):
        self.load_html(EnumHTML.MAIN)
        self.load_init_css()
        self.load_init_js()

    def load_init_css(self):
        """ 初期化時に読み込まれるCSS """
        self.load_css(EnumCSS.BOOTSTRAP)
        self.load_css(EnumCSS.MAIN)

    def load_init_js(self):
        """ 初期化時に読み込まれるJS """
        self.load_js(EnumJS.BOOTSTRAP)
        self.load_js(EnumJS.MAIN)

    def run(self):
        """ アプリを開く """
        webview.start(self.thread_func, gui=S_APP_WEB_ENGINE, debug=S_DEBUG_FLAG)

    def load_js(self, js_enum: EnumJS):
        """ 指定したJSを読み込む関数 """
        _js_text = self.load_gui_data(S_GUI_JS_DIR_NAME, js_enum.value)
        self.window.evaluate_js(_js_text)

    def load_css(self, css_enum: EnumCSS):
        """ 指定したCSSを読み込む関数 """
        _css_text = self.load_gui_data(S_GUI_CSS_DIR_NAME, css_enum.value)
        self.window.load_css(_css_text)

    def load_html(self, html_enum: EnumHTML):
        """ 指定したHTMLの画面に遷移する関数 """
        _html_text = self.load_gui_data(S_GUI_HTML_DIR_NAME, html_enum.value)
        self.window.load_html(_html_text)

    def load_gui_data(self, *gui_file_path: str) -> str:
        """ 指定したパスのデータを取得する関数 """
        _path = Path(S_GUI_DIR_PATH, *gui_file_path)
        return _path.read_text(encoding=S_DEFAULT_ENCODING)

def main():
    """ メイン関数 """
    # フォルダの存在確認と作成
    make_dir_need_dirs()
    main_window = WebViewWindow()
    main_window.run() # ウィンドウを開く

if __name__ == '__main__':
    main()