import sys
from random import randint
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# ダイスロール
def DiceRoll(diceNum: int, diceMax: int, plus: int):
  for i in range(diceNum):
    plus += randint(1, diceMax)
  return plus

# 敵の名前の生成処理
def EnemyNameEdit():
  tempTXT = 'EnemyNo：['
  x = randint(0, 65535)
  x = hex(x)[2:]
  x = x.zfill(4)
  tempTXT += x
  tempTXT += ']'
  return tempTXT

# メインテキストボックスの位置・サイズを指定
mainTextBoxPos = [480, 10]  # メインテキストボックスの横位置,縦位置
mainTextBoxSize = [320, 600]  # メインテキストボックスの横幅、縦幅

statusTextBoxSize_Ver = mainTextBoxSize[1] / 2 - 5

# ステータス表示テキストボックスの位置・サイズ指定
# プレイヤーステータス表示テキストボックスの横位置,縦位置
P_statusTextBoxPos = [mainTextBoxPos[0] + mainTextBoxSize[0] + 10, 10]
E_statusTextBoxPos = [mainTextBoxPos[0] + mainTextBoxSize[0] + 10,
                      statusTextBoxSize_Ver + 20]  # 敵ステータス表示テキストボックスの横位置,縦位置
statusTextBoxSize = [320, statusTextBoxSize_Ver]  # プレイヤーステータス表示テキストボックスの横幅、縦幅

# メインウィンドウのサイズを指定（px単位）
mainWindowSize = [P_statusTextBoxPos[0] + statusTextBoxSize[0] + 10,
                  mainTextBoxPos[1] + mainTextBoxSize[1] + 10]  # ウィンドウの横幅,縦幅

# プレイヤー守備成功時のテキスト
playerAvoid = ['敵の攻撃を回避！\n',
               '敵の攻撃を弾いた！\n',
               '敵に反撃した！\n']

# 敵守備成功時のテキスト
enemyAvoid = ['しかし回避されてしまった！\n',
              'しかし弾かれてしまった！\n',
              '反撃されてしまった！\n']

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
attacks = [Attack('こぶし（パンチ）', 80, 1, 5, False, False, '手を使った攻撃。チョップや張り手も含む。'),
           Attack('キック', 40, 1, 8, False, False,
                  '脚を使った攻撃。回し蹴りやかかと落としやドロップキックも含む。'),
           Attack('頭突き', 80, 1, 3, True, False, '頭を使った攻撃。驚くほど素早く攻撃できる。'),
           Attack('投擲', 80, 1, 3, False, True, '物を投げる攻撃。石を拾って投げる。'),
           Attack('拳銃', 40, 1, 8, True, True, '弾が一発づつ発射されるタイプの銃を扱う攻撃。弾がないと使えない。')]

# 守備技能を扱うクラスの定義
class Defence():
  def __init__(self, name: str, successRate: str, explanation: str):
    self.name = name                # 防御技能の名前
    self.successRate = successRate  # 成功率
    self.explanation = explanation  # 説明文

# 防御技能一覧のインスタンスの生成
defences = [Defence('回避', '(相手のロールの出目 + 50)', '自分への攻撃を避ける技能。失敗するとすべてのダメージを受ける。'),
            Defence('防御', '((5 - ダメージ量) * 20)',
                    'ダメージを受け止める技能。失敗しても 5 - 出目 / 20(小数点以下切り捨て)だけダメージを減らす。'),
            Defence('反撃', '80', '相手の攻撃を受けつつ、反撃する技能。相手が近距離攻撃をしないと成功しない(ダメージ量1D4)')]

# 能力値を扱うクラスの生成（本ゲームではCOC6版（クトゥルフ神話RPG）の能力値決定システムを採用しています。)
class Status():
  def __init__(self, name: str, state_STR: int, state_CON: int, state_SIZ: int, state_DEX: int, state_APP: int, state_INT: int, state_POW: int, state_EDU: int, state_HP: int, bullets: int):
    self.name = name
    self.state_STR = state_STR
    self.state_CON = state_CON
    self.state_SIZ = state_SIZ
    self.state_DEX = state_DEX
    self.state_APP = state_APP
    self.state_INT = state_INT
    self.state_POW = state_POW
    self.state_EDU = state_EDU
    self.state_HP = state_HP
    self.bullets = bullets

# 敵のステータスのインスタンスの生成
enemyStatus = Status(EnemyNameEdit(),
                     DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 0),
                     DiceRoll(2, 6, 6),
                     DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 0),
                     DiceRoll(2, 6, 6),
                     DiceRoll(3, 6, 0),
                     DiceRoll(3, 6, 6),
                     0,
                     3)
# state_HPは他のステータスに依存し決定するため後から生成
enemyStatus.state_HP = round(
    (enemyStatus.state_CON + enemyStatus.state_SIZ) / 2)

# プレイヤーのステータスのインスタンスの生成
playerStatus = Status('Player (YOU)',
                      DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 0),
                      DiceRoll(2, 6, 6),
                      DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 0),
                      DiceRoll(2, 6, 6),
                      DiceRoll(3, 6, 0),
                      DiceRoll(3, 6, 6),
                      0,
                      3)
# state_HPは他のステータスに依存し決定するため後から生成
playerStatus.state_HP = round(
    (playerStatus.state_CON + playerStatus.state_SIZ) / 2)

# 先行後攻の算出
randomDEX = False
playerFirst = False
if enemyStatus.state_DEX < playerStatus.state_DEX:
  playerFirst = True
elif enemyStatus.state_DEX == playerStatus.state_DEX:
  randomDEX = True
  myDiceResult = 0
  enemyDiceResult = 0
  while myDiceResult == enemyDiceResult:
    myDiceResult = DiceRoll(1, 100, 0)
    enemyDiceResult = DiceRoll(1, 100, 0)
  if myDiceResult < enemyDiceResult:
    playerFirst = True

# 自分と敵のDEX・先行/後攻を知らせる文章の生成
if randomDEX:
  if playerFirst:
    fastSecondTXT = f'プレイヤーのDEX({playerStatus.state_DEX}) ＝ 敵のDEX({enemyStatus.state_DEX}) \n\
ダイスバトル：プレイヤー({myDiceResult}) ＜ 敵({enemyDiceResult})｜あなたが先行'
  else:
    fastSecondTXT = f'プレイヤーのDEX({playerStatus.state_DEX}) ＝ 敵のDEX({enemyStatus.state_DEX}) \n\
ダイスバトル：プレイヤー({myDiceResult}) ＞ 敵({enemyDiceResult})｜敵が先行'
else:
  if playerFirst:
    fastSecondTXT = f'プレイヤーのDEX({playerStatus.state_DEX}) ＞ 敵のDEX({enemyStatus.state_DEX})｜あなたが先行'
  else:
    fastSecondTXT = f'プレイヤーのDEX({playerStatus.state_DEX}) ＜ 敵のDEX({enemyStatus.state_DEX})｜敵が先行'

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
