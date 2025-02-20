import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# ランダム数字抽出 ####
def Dice_1D100():
  x = r.randint(1, 100)
  return x

# メインウィンドウのサイズを指定（px単位）
mainWindowSize = [1012, 480]   # ウィンドウの横幅,縦幅

# 戦闘技能ウィンドウのサイズを指定（px単位）#?main.pyでは未使用。failedCode(失敗したコード)にて使用。(改めて見て参考にすることがあるため残している。)
AttackSelectWindowSize = [420, 120]

# 戦闘技能を扱うクラスの定義
class Attack():
  def __init__(self, name: str, successRate: int, dice: int, damage: int, fast: bool, indirect: bool):
    self.name = name         # 戦闘技能の名前
    self.successRate = successRate  # 成功率
    self.dice = dice         # ダイス数
    self.damage = damage  # 最大ダメージ量
    self.fast = fast  # 先制攻撃の制御
    self.indirect = indirect  # 遠距離攻撃の制御

# 戦闘技能一覧のインスタンスの生成
attacks = [Attack('こぶし（パンチ）', 50, 1, 3, False, False),
           Attack('キック', 25, 1, 6, False, False),
           Attack('頭突き', 30, 1, 4, True, False),
           Attack('投擲', 25, 1, 4, False, True),
           Attack('拳銃', 20, 1, 8, True, True),]

# ?以下、用意したけど使う予定はなし（時間があれば追加予定）
# 特殊攻撃を扱うクラスの定義
class SpecialAttack():
  def __init__(self, name: str, successRate: int, effect: str):
    self.name = name
    self.successRate = successRate
    self.effect = effect

# 特殊攻撃一覧のインスタンスの生成
SpecialAttacks = [SpecialAttack('マーシャルアーツ', 30, '素手での攻撃（こぶし、キック、組みつき、頭突き）のダメージ２倍'),
                  SpecialAttack('頭狙い', 50, '武器での攻撃（投擲、拳銃）のダメージ２倍、失敗すると外れる')]
