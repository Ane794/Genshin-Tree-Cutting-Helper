import argparse

from pyautogui import *
from ruamel import yaml


def run(points: list, use_item_key: str = 'z', paimon_key: str = 'esc'):
    """
    執行自動砍樹.

    :param points: [
            [`退出游戲` 按鈕 X 坐標, `退出游戲` 按鈕 Y 坐標],
            [`確認` 按鈕 X 坐標, `確認` 按鈕 Y 坐標]
        ]
    :param use_item_key: `使用小道具` 的鍵盤按鍵
    :param paimon_key: `打開派蒙菜單` 的鍵盤按鍵
    """
    _ = 1
    while 1:
        press(use_item_key)
        print(f'\r{_}', end='')
        sleep(0.5)
        press(paimon_key)
        sleep(1)
        # 點擊 `退出游戲` 按鈕.
        click(*points[0])
        sleep(0.5)
        # 單擊 `確認` 按鈕.
        click(*points[1])
        sleep(12)
        # 單擊 `確認` 按鈕的位置.
        click(*points[1])
        sleep(10)
        _ += 1


def get_positions():
    """
    獲取 `退出游戲` 和 `確認` 按鈕的位置.

    :return: [
            [`退出游戲` 按鈕 X 坐標, `退出游戲` 按鈕 Y 坐標],
            [`確認` 按鈕 X 坐標, `確認` 按鈕 Y 坐標]
        ]
    """
    _positions = []
    for _ in ['退出游戲', '確認']:
        print(f'倒計時 3 秒後, 將獲取鼠標所在位置, 作爲 `{_}` 按鈕的坐標.')
        os.system('pause')
        for _timer in range(3, 0, -1):
            sleep(1)
        _p = get_position()
        _positions.append(_p)
        print(f'`{_}` 按鈕的坐標:', _p)
    return _positions


def get_position():
    """
    獲取鼠標所在位置的坐標.

    :return: 鼠標所在的 X 坐標, 鼠標所在的 Y 坐標
    """

    _x, _y = position()
    return _x, _y


if __name__ == '__main__':
    CONFIG_PATH = 'config.yml'

    # 解析參數.
    parser = argparse.ArgumentParser(prog='Genshin Tree Cutting')
    parser.add_argument(
        '-s', '--set',
        action='store_true',
        help='set point positions and exit',
    )
    args = parser.parse_args()

    # 讀取 `config.yml`.
    try:
        config_file = open(CONFIG_PATH, encoding='UTF-8')
        config = yaml.safe_load(config_file)
        config_file.close()

        if not config:
            config = {}
    except IOError as err:
        print(err)
        config = {}

    # -s, --set; set point positions and exit
    if args.set:
        config['points'] = get_positions()
        config_file = open(CONFIG_PATH, 'w', encoding='UTF-8')
        yaml.dump(config, config_file, Dumper=yaml.RoundTripDumper)
        config_file.close()
        exit(0)

    # 運行自動砍樹.
    sleep(2)
    run(config['points'])
