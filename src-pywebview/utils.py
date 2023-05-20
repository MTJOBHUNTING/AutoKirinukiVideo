from typing import Set, List, Tuple
from pathlib import Path
from settings import *

# すべてのファイル(ファイルタイプ)
FILE_TYPE_ALL: str = 'All files (*.*)'

# 実行時に必要となるフォルダ
S_NEED_DIR_PATH_LIST: List[Path] = [
    Path(S_PROJECT_FILE_OUTPUT), 
    Path(S_TEMP_DIR_PATH),
    Path(S_TEMP_DIR_PATH, S_TEMP_INPUT_DIR_NAME),
    Path(S_TEMP_DIR_PATH, S_TEMP_OUTPUT_DIR_NAME)
]
def get_file_types(file_type_name: str, file_extension_set: Set[str]) -> Tuple[str, str]:
    """ ファイルタイプの名前と拡張子からファイル選択ダイアログで使用するための、ファイルタイプを取得する関数 """
    add_file_type: str = f'{file_type_name} (*.{";*.".join(file_extension_set)})'

    return (add_file_type, FILE_TYPE_ALL)

def make_dir_need_dirs():
    """ 実行に必要なフォルダが存在するか確認し、存在しなければ作成する """
    for need_dir_path in S_NEED_DIR_PATH_LIST:
        # フォルダが存在しなければ作成
        need_dir_path.mkdir(exist_ok=True)

def get_dir_all_file_pathes(target_dir_path: Path) -> List[Path]:
    """ 
    指定したディレクトリ内に存在する、すべてのファイルリストパスを返す。
    (サブディレクトリの中にあるファイルも含む)
    """
    # 結果となるファイルパスリスト
    result_path_list = list()

    # 指定したディレクトリの中にある(ファイル, フォルダ)を取得する
    for item in target_dir_path.iterdir():
        # アイテムがディレクトリなら、再帰的にサブディレクトリの中のファイルを取得し、結果リストに追加する
        if item.is_dir():
            result_path_list += get_dir_all_file_pathes(item)
        # アイテムがファイルなら、結果リストに追加する
        elif item.is_file():
            result_path_list.append(item)

    # 結果を返す
    return result_path_list
