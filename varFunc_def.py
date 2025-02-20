import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# ランダム数字抽出 ####
def Dice_1D100():
  x = r.randint(1, 100)
  return x

# テキストボックスの位置・サイズを指定
textBoxPos = [480, 10]  # テキストボックスの横位置,縦位置
textBoxSize = [620, 420]  # テキストボックスの横幅、縦幅

# メインウィンドウのサイズを指定（px単位）
mainWindowSize = [textBoxPos[0] + textBoxSize[0] + 10,
                  textBoxPos[1] + textBoxSize[1] + 10 + 30]   # ウィンドウの横幅,縦幅

# 戦闘技能ウィンドウのサイズを指定（px単位）#?main.pyでは未使用。failedCode(失敗したコード)にて使用。(改めて見て参考にすることがあるため残している。)
AttackSelectWindowSize = [420, 120]

# 戦闘技能を扱うクラスの定義
class Attack():
  def __init__(self, name: str, successRate: int, dice: int, damage: int, fast: bool, indirect: bool, explanation: str):
    self.name = name         # 戦闘技能の名前
    self.successRate = successRate  # 成功率
    self.dice = dice         # ダイス数
    self.damage = damage  # 最大ダメージ量
    self.fast = fast  # 先制攻撃の制御
    self.indirect = indirect  # 遠距離攻撃の制御
    self.explanation = explanation  # 説明文

# 戦闘技能一覧のインスタンスの生成
attacks = [Attack('こぶし（パンチ）', 80, 1, 3, False, False, '手を使った攻撃。チョップや張り手も含む。'),
           Attack('キック', 40, 1, 6, False, False,
                  '脚を使った攻撃。回し蹴りやかかと落としやドロップキックも含む。'),
           Attack('頭突き', 50, 1, 4, True, False, '頭を使った攻撃。驚くほど素早く攻撃できる。'),
           Attack('投擲', 40, 1, 4, False, True, '物を投げる攻撃。石を拾って投げる。'),
           Attack('拳銃', 30, 1, 8, True, True, '弾が一発づつ発射されるタイプの銃を扱う攻撃。弾がないと使えない。')]

class Defence():
  def __init__(self, name: str, successRate: str, explanation: str, srTest: int):
    self.name = name                # 防御技能の名前
    self.successRate = successRate  # 成功率
    self.explanation = explanation  # 説明文
    self.srTest = srTest            # 成功率の一時テスト用

# 防御技能一覧のインスタンスの生成
defences = [Defence('回避', '(相手のロールの出目 + 50)', '自分への攻撃を避ける技能。失敗するとすべてのダメージを受ける。', 75),
            Defence('防御', '((10 - ダメージ量) * 10)',
                    'ダメージを受け止める技能。失敗しても10 - 出目 / 10(小数点以下切り下げ)だけダメージを減らす。', 75),
            Defence('反撃', '80', '相手の攻撃を受け、反撃する技能。相手が近距離攻撃をしないと成功しない(ダメージ量1D6)', 80)]

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
