import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# ダイスロール
def DiceRoll(diceNum: int, diceMax: int, plus: int):
  for i in range(diceNum):
    plus += r.randint(1, diceMax)
  return plus

# 敵の名前の生成処理
def EnemyNameEdit():
  tempTXT = 'EnemyNo：['
  x = r.randint(0, 65535)
  x = hex(x)[2:]
  x = x.zfill(4)
  tempTXT += x
  tempTXT += ']'
  return tempTXT

# テキストボックスの位置・サイズを指定
textBoxPos = [480, 10]  # テキストボックスの横位置,縦位置
textBoxSize = [620, 420]  # テキストボックスの横幅、縦幅

# メインウィンドウのサイズを指定（px単位）
mainWindowSize = [textBoxPos[0] + textBoxSize[0] + 10,
                  textBoxPos[1] + textBoxSize[1] + 10 + 30]   # ウィンドウの横幅,縦幅

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

# 守備技能を扱うクラスの定義
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

# 能力値を扱うクラスの生成（本ゲームではCOC6版（クトゥルフ神話RPG）の能力値決定システムを採用しています。)
class Status():
  def __init__(self, state_STR: int, state_CON: int, state_SIZ: int, state_DEX: int, state_APP: int, state_INT: int, state_POW: int, state_EDU: int, state_HP: int):
    # self.name = name
    self.state_STR = state_STR
    self.state_CON = state_CON
    self.state_SIZ = state_SIZ
    self.state_DEX = state_DEX
    self.state_APP = state_APP
    self.state_INT = state_INT
    self.state_POW = state_POW
    self.state_EDU = state_EDU
    self.state_HP = state_HP

# ? プレイヤー名は表示しない予定のため一旦外に出しておく。
enemyName = EnemyNameEdit()

# 敵のステータスのインスタンスの生成
enemyStatus = Status(DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 0),
                     DiceRoll(2, 6, 6),
                     DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 0),
                     DiceRoll(2, 6, 6),
                     DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 6),
                     0)
# state_HPは他のステータスに依存し決定するため後から生成
enemyStatus.state_HP = round(
    (enemyStatus.state_CON + enemyStatus.state_SIZ) / 2)

# プレイヤーのステータスのインスタンスの生成
playerStatus = Status(DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 0),
                      DiceRoll(2, 6, 6),
                      DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 0),
                      DiceRoll(2, 6, 6),
                      DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 6),
                      0)
# state_HPは他のステータスに依存し決定するため後から生成
playerStatus.state_HP = round(
    (enemyStatus.state_CON + enemyStatus.state_SIZ) / 2)

# テキストボックスに表示するログのテンプレ一覧を扱うクラスの生成
class LogTemplate():
  def __init__(self, encounterLog: str,
               ):
    self.encounterLog = encounterLog

# テキストボックスに表示するログのテンプレ一覧のインスタンスの生成
logTemplate = LogTemplate(f' {enemyName} が現れた！\n')

# ? 以下、用意したけど使う予定はなし（時間があれば追加予定）
# 特殊攻撃を扱うクラスの定義
class SpecialAttack():
  def __init__(self, name: str, successRate: int, effect: str):
    self.name = name
    self.successRate = successRate
    self.effect = effect

# 特殊攻撃一覧のインスタンスの生成
SpecialAttacks = [SpecialAttack('マーシャルアーツ', 30, '素手での攻撃（こぶし、キック、組みつき、頭突き）のダメージ２倍'),
                  SpecialAttack('頭狙い', 50, '武器での攻撃（投擲、拳銃）のダメージ２倍、失敗すると外れる')]
