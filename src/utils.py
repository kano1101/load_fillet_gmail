import re

def col_name_to_index(col_name):
    """列名（'A'、'B'、...、'AA'、等）を0から始まるインデックスに変換する"""
    index = 0
    for char in col_name:
        index = index * 26 + (ord(char) - ord('A') + 1)
    return index - 1


def index_to_col_name(index):
    """0から始まるインデックスを列名（'A'、'B'、...、'AA'等）に変換する"""
    col_name = ''
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        col_name = chr(65 + remainder) + col_name
    return col_name


def to_column_values(arr):
    return [[elem] for elem in arr]


def replace_whitespace(text):
    return re.sub(r'\s', ' ', text)


def max_value_in_column(values, index) -> int:
    max_val = values[0][index]  # 最大値を初期化（最初の行の指定列の値で初期化）
    for row in values:
        if row[index] > max_val:
            max_val = row[index]  # より大きな値が見つかった場合、最大値を更新
    return int(max_val)
