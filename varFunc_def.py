import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# ランダム数字抽出 ####
def Dice_1D100():
  x = r.randint(1, 100)
  return x

# ウィンドウサイズを指定（px単位）
mainWindowSize = [640, 480]   # ウィンドウの横幅,縦幅

# 攻撃手段を扱うクラスの定義
class Attack():
  def __init__(self, name: str, successRate: int, dice: int, damage: int, fast: bool, indirect: bool):
    self.name = name         # 攻撃技能
    self.successRate = successRate  # 成功率
    self.dice = dice         # ダイス数
    self.damage = damage  # 最大ダメージ量
    self.fast = fast  # 先制攻撃の制御
    self.indirect = indirect  # 遠距離攻撃の制御

# 攻撃一覧のインスタンスの生成
Attacks = [Attack('こぶし（パンチ）', 50, 1, 3, False, True),
           Attack('キック', 25, 1, 6, False, True),
           Attack('頭突き', 30, 1, 4, True, False),
           Attack('投擲', 25, 1, 4, False, True),
           Attack('拳銃', 20, 1, 8, True, True),]
