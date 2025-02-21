import sys
from random import randint
from math import floor
from time import sleep
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt
import varFunc_def as vfd

# * MainWindowクラス定義
class MainWindow(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    # 事前に敵の初めの行動を一度決めておく
    self.enemyAttackCtrl = randint(1, len(vfd.attacks)) - 1
    self.enemyDefenceCtrl = randint(1, len(vfd.defences)) - 1

    # 先攻後攻の制御のための定義
    if vfd.playerFirst:
      self.playerTurn = True
    else:
      self.playerTurn = False

    # 戦闘・守備技能未選択時のラジオボタンのIDの設定
    self.rbId = len(vfd.attacks)
    self.rbId_defence = len(vfd.defences)

    # 守備技能未選択時のラジオボタンのIDの設定
    self.rbId_defence = len(vfd.defences)

    # ウィンドウサイズの固定
    self.setFixedSize(vfd.mainWindowSize[0], vfd.mainWindowSize[1])

    # ウィンドウの位置をスクリーン中央に設定
    rect = Qc.QRect()
    rect.setSize(Qc.QSize(vfd.mainWindowSize[0], vfd.mainWindowSize[1]))
    rect.moveCenter(app.primaryScreen().availableGeometry().center())
    self.setGeometry(rect)

    # ウィンドウ名
    self.setWindowTitle('Main')

    # メインレイアウトの設定
    central_widget = Qw.QWidget(self)
    self.setCentralWidget(central_widget)
    mainLayout = Qw.QVBoxLayout(central_widget)  # 要素を垂直配置
    mainLayout.setAlignment(Qc.Qt.AlignmentFlag.AlignTop)  # 上寄せ
    mainLayout.setContentsMargins(15, 10, 10, 10)

    # 戦闘技能選択テキストの設定
    attackSelectTXT = Qw.QLabel('どう攻撃する？')  # 質問を表示する
    mainLayout.addWidget(attackSelectTXT)

    # ラジオボタンを格納する画面表示上のコンテナ
    rbLayout_attack = Qw.QHBoxLayout()  # 要素を水平配置
    rbLayout_attack.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft)  # 左寄せ
    mainLayout.addLayout(rbLayout_attack)

    # ラジオボタンの生成と設定
    self.attackChoices = Qw.QButtonGroup(self)  # 選択肢のグループ
    for i, attacks in enumerate(vfd.attacks, 1):
      rb = Qw.QRadioButton(self)  # 一つずつラジオボタンを作成する
      # 1番目のラジオボタンを初期入力として設定
      if i == 1:
        rb.setChecked(True)
      rb.setText(attacks.name)
      rbLayout_attack.addWidget(rb)  # レイアウトに追加
      self.attackChoices.addButton(rb, i)  # 選択グループに追加
    # ラジオボタンがクリックされたら下の方のテクストの変化もさせる
    self.attackChoices.buttonClicked.connect(self.AttackRBClicked)
    # 攻撃の説明文の追加
    self.blankTXT = Qw.QLabel('', self)
    mainLayout.addWidget(self.blankTXT)  # 空白を挟む
    self.attackLabelTXT = Qw.QLabel('', self)
    mainLayout.addWidget(self.attackLabelTXT)
    self.attackExp = Qw.QLabel('', self)
    mainLayout.addWidget(self.attackExp)
    self.AttackRBClicked()

    # 防御技能選択テキストの設定
    self.blankTXT = Qw.QLabel('')
    mainLayout.addWidget(self.blankTXT)
    self.blankTXT = Qw.QLabel('')
    mainLayout.addWidget(self.blankTXT)  # 空白を2つ挟む
    defenceSelectTXT = Qw.QLabel('守備はどうする？')  # 質問を表示する
    mainLayout.addWidget(defenceSelectTXT)

    # ラジオボタンを格納する画面表示上のコンテナ
    rbLayout_defence = Qw.QHBoxLayout()  # 要素を水平配置
    rbLayout_defence.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft)  # 左寄せ
    mainLayout.addLayout(rbLayout_defence)

    # ラジオボタンの生成と設定
    self.defenceChoices = Qw.QButtonGroup(self)  # 選択肢のグループ
    for i, defences in enumerate(vfd.defences, 1):
      rb = Qw.QRadioButton(self)  # 一つずつラジオボタンを作成する
      # 1番目のラジオボタンを初期入力として設定
      if i == 1:
        rb.setChecked(True)
      rb.setText(defences.name)
      rbLayout_defence.addWidget(rb)  # レイアウトに追加
      self.defenceChoices.addButton(rb, i)  # 選択グループに追加
    # ラジオボタンがクリックされたら下の方のテクストの変化もさせる
    self.defenceChoices.buttonClicked.connect(self.DefenceRBClicked)
    # 守備の説明文の追加
    self.blankTXT = Qw.QLabel('')
    mainLayout.addWidget(self.blankTXT)  # 空白を挟む
    self.defenceLabelTXT = Qw.QLabel('', self)
    mainLayout.addWidget(self.defenceLabelTXT)
    self.defenceExp = Qw.QLabel('', self)
    mainLayout.addWidget(self.defenceExp)  # 空白を挟む
    self.DefenceRBClicked()

    # 「実行」ボタンの生成と設定
    self.btn_run = Qw.QPushButton('準備完了', self)
    self.btn_run.setGeometry(120, 380, 250, 60)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('', self)
    self.tb_log.setGeometry(
        vfd.textBoxPos[0], vfd.textBoxPos[1], vfd.textBoxSize[0], vfd.textBoxSize[1])
    self.tb_log.setReadOnly(True)
    if self.playerTurn:
      self.tb_log.setPlainText(
          f'あなたのターンです。\n相手は 成功値({vfd.enemyName} が現れた！\n戦闘技能と防御技能を選択して戦いに備えよう！\n' + vfd.fastSecondTXT)
    else:
      self.tb_log.setPlainText(
          f'相手は 成功値({vfd.attacks[self.enemyAttackCtrl].successRate}) の攻撃を準備している。\n {vfd.enemyName} が現れた！\n戦闘技能と防御技能を選択して戦いに備えよう！\n' + vfd.fastSecondTXT)

    # ステータスバー
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage('～プログラム起動中～')

  # 戦闘技能選択変更時の処理
  def AttackRBClicked(self):
    self.rbId_attack = self.attackChoices.checkedId() - 1
    if 0 <= self.rbId_attack < len(vfd.attacks):
      TempTXT = f'成功率：{vfd.attacks[self.rbId_attack].successRate}％｜ダイス：{vfd.attacks[self.rbId_attack].dice}d{vfd.attacks[self.rbId_attack].damage}'
      if vfd.attacks[self.rbId_attack].fast:
        TempTXT += ' | 速度：高速（回避無効）'
      else:
        TempTXT += ' | 速度：通常（回避有効）'
      if vfd.attacks[self.rbId_attack].indirect:
        TempTXT += ' | 距離：遠距離（反撃無効）'
      else:
        TempTXT += ' | 距離：近距離（反撃有効）'
    else:
      TempTXT = 'error! 異常な選択です。制作者に報告してください。'
    self.attackLabelTXT.setText(TempTXT)
    self.attackExp.setText(vfd.attacks[self.rbId_attack].explanation)

  # 守備技能選択変更時の処理
  def DefenceRBClicked(self):
    self.rbId_defence = self.defenceChoices.checkedId() - 1
    if 0 <= self.rbId_defence < len(vfd.defences):
      TempTXT = f'成功率：{vfd.defences[self.rbId_defence].successRate}％ (0を下回る場合は0％、100を上回る場合は100％)'
    else:
      TempTXT = 'error! 異常な選択です。制作者に報告してください。'
    self.defenceLabelTXT.setText(TempTXT)
    self.defenceExp.setText(vfd.defences[self.rbId_defence].explanation)

  # プレイヤーの攻撃の処理
  def MyAttack(self):
    success = False
    myDiceResult = vfd.DiceRoll(1, 100, 0)
    if vfd.attacks[self.rbId_attack].successRate >= myDiceResult:
      success = True
      if 5 >= myDiceResult:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ≧ {myDiceResult}　クリティカル（決定的成功）\n攻撃力二倍！\n'
        mainDamageTemp = vfd.DiceRoll(
            vfd.attacks[self.rbId_attack].dice * 2, vfd.attacks[self.rbId_attack].damage, 0)
        rollResultTXT += f'2D{vfd.attacks[self.rbId_attack].damage} => {mainDamageTemp}\n'
      else:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ≧ {myDiceResult}　成功\n'
        mainDamageTemp = vfd.DiceRoll(
            vfd.attacks[self.rbId_attack].dice, vfd.attacks[self.rbId_attack].damage, 0)
        rollResultTXT += f'1D{vfd.attacks[self.rbId_attack].damage} => {mainDamageTemp}\n'
    else:
      if 95 >= myDiceResult:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ＜ {myDiceResult}　失敗\n'
      else:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ＜ {myDiceResult}　ファンブル（致命的失敗）\n転んで1ダメージ...\n'
    # ここから敵側の処理
    if success:
      if self.enemyDefenceCtrl == 0 and vfd.attacks[self.rbId_attack].fast:
        rollResultTXT += f'攻撃が早すぎて回避することができない！\n攻撃は敵に命中した！({mainDamageTemp}ダメージ)\n'
      elif self.enemyDefenceCtrl == 2 and vfd.attacks[self.rbId_attack].indirect:
        rollResultTXT += f'距離が遠すぎて反撃することができない！\n攻撃は敵に命中した！({mainDamageTemp}ダメージ)\n'
      else:
        successRateDefTemp = [myDiceResult + 50,
                              (5 - mainDamageTemp) * 20,
                              80]
        for i in range(len(successRateDefTemp)):
          if successRateDefTemp[i] <= 0:
            successRateDefTemp[i] = 0
          elif successRateDefTemp[i] >= 100:
            successRateDefTemp[i] = 100
        enemyDiceResult = vfd.DiceRoll(1, 100, 0)
        if successRateDefTemp[self.enemyDefenceCtrl] >= enemyDiceResult:
          rollResultTXT += f'敵：{vfd.defences[self.enemyDefenceCtrl].name}（{successRateDefTemp[self.enemyDefenceCtrl]}） ≧ {enemyDiceResult}　成功\n'
          rollResultTXT += vfd.enemyAvoid[self.enemyDefenceCtrl]
          if self.enemyDefenceCtrl == 2:
            counterDamageTemp = vfd.DiceRoll(1, 4, 0)
            rollResultTXT += f'1D4 => {counterDamageTemp}ダメージ\n'
        else:
          rollResultTXT += f'敵：{vfd.defences[self.enemyDefenceCtrl].name}（{successRateDefTemp[self.enemyDefenceCtrl]}） ＜ {enemyDiceResult}　失敗\n'
          if self.enemyDefenceCtrl == 1:
            mainDamageTemp -= floor(5 - enemyDiceResult / 20)
          rollResultTXT += f'攻撃は敵に命中した！({mainDamageTemp}ダメージ)\n'
    rollResultTXT += "\n\n"
    return rollResultTXT

  # 敵の攻撃の処理
  def EnemyAttack(self):
    success = False
    enemyDiceResult = vfd.DiceRoll(1, 100, 0)
    if vfd.attacks[self.enemyAttackCtrl].successRate >= enemyDiceResult:
      success = True
      if 5 >= enemyDiceResult:
        rollResultTXT = f'敵：{vfd.attacks[self.enemyAttackCtrl].name}（{vfd.attacks[self.enemyAttackCtrl].successRate}） ≧ {enemyDiceResult}　クリティカル（決定的成功）\n攻撃力二倍！\n'
        mainDamageTemp = vfd.DiceRoll(
            vfd.attacks[self.enemyAttackCtrl].dice * 2, vfd.attacks[self.enemyAttackCtrl].damage, 0)
        rollResultTXT += f'2D{vfd.attacks[self.enemyAttackCtrl].damage} => {mainDamageTemp}\n'
      else:
        rollResultTXT = f'敵：{vfd.attacks[self.enemyAttackCtrl].name}（{vfd.attacks[self.enemyAttackCtrl].successRate}） ≧ {enemyDiceResult}　成功\n'
        mainDamageTemp = vfd.DiceRoll(
            vfd.attacks[self.enemyAttackCtrl].dice, vfd.attacks[self.enemyAttackCtrl].damage, 0)
        rollResultTXT += f'1D{vfd.attacks[self.enemyAttackCtrl].damage} => {mainDamageTemp}\n'
    else:
      if 95 >= enemyDiceResult:
        rollResultTXT = f'敵：{vfd.attacks[self.enemyAttackCtrl].name}（{vfd.attacks[self.enemyAttackCtrl].successRate}） ＜ {enemyDiceResult}　失敗\n'
      else:
        rollResultTXT = f'敵：{vfd.attacks[self.enemyAttackCtrl].name}（{vfd.attacks[self.enemyAttackCtrl].successRate}） ＜ {enemyDiceResult}　ファンブル（致命的失敗）\n転んで1ダメージ...\n'
    # ここからプレイヤー側の処理
    if success:
      if self.rbId_defence == 0 and vfd.attacks[self.enemyAttackCtrl].fast:
        rollResultTXT += f'攻撃が早すぎて回避することができない！\n敵の攻撃を受けてしまった！({mainDamageTemp}ダメージ)\n'
      elif self.rbId_defence == 2 and vfd.attacks[self.enemyAttackCtrl].indirect:
        rollResultTXT += f'距離が遠すぎて反撃することができない！\n敵の攻撃を受けてしまった！({mainDamageTemp}ダメージ)\n'
      else:
        successRateDefTemp = [enemyDiceResult + 50,
                              (5 - mainDamageTemp) * 20,
                              80]
        for i in range(len(successRateDefTemp)):
          if successRateDefTemp[i] <= 0:
            successRateDefTemp[i] = 0
          elif successRateDefTemp[i] >= 100:
            successRateDefTemp[i] = 100
        myDiceResult = vfd.DiceRoll(1, 100, 0)
        if successRateDefTemp[self.rbId_defence] >= myDiceResult:
          rollResultTXT += f'自分：{vfd.defences[self.rbId_defence].name}（{successRateDefTemp[self.rbId_defence]}） ≧ {myDiceResult}　成功\n'
          rollResultTXT += vfd.playerAvoid[self.rbId_defence]
          if self.rbId_defence == 2:
            counterDamageTemp = vfd.DiceRoll(1, 4, 0)
            rollResultTXT += f'1D4 => {counterDamageTemp}ダメージ\n'
        else:
          rollResultTXT += f'自分：{vfd.defences[self.rbId_defence].name}（{successRateDefTemp[self.rbId_defence]}） ＜ {myDiceResult}　失敗\n'
          if self.rbId_defence == 1:
            mainDamageTemp -= floor(5 - myDiceResult / 20)
          rollResultTXT += f'敵の攻撃を受けてしまった！({mainDamageTemp}ダメージ)\n'
    rollResultTXT += "\n\n"
    return rollResultTXT

  # 「実行」ボタンの押下処理
  def btn_run_clicked(self):

    # 一時保存用のテキストの初期化
    tempText = ''

    # 正常に動作したかの確認用
    normalAct = False

    if self.playerTurn:
      if self.rbId_attack == 4 and vfd.playerStatus.Bullets == 0:
        tempText += 'error! 弾切れです。他の技能を使用してください。\n'
      elif 0 <= self.rbId_attack < len(vfd.attacks):
        normalAct = True
      elif self.rbId_attack == len(vfd.attacks):
        tempText += 'error! 戦闘技能が選択されていません。\n'
      else:
        tempText += 'error! 戦闘技能が異常な選択です。制作者に報告し、再度選択するか進行が不可能な場合はゲームを再起動してください。\n'
    else:
      if 0 <= self.rbId_defence < len(vfd.defences):
        normalAct = True
      elif self.rbId_defence == len(vfd.defences):
        tempText += 'error! 守備技能が選択されていません。\n'
      else:
        tempText += 'error! 守備技能が異常な選択です。制作者に報告し、再度選択するか進行が不可能な場合はゲームを再起動してください。\n'

    if normalAct:
      # プログレスバーダイアログ (演出効果) の表示
      rollTheDice = ['  1D100抽出中 ~ ―  ',
                     '  1D100抽出中 ~ ＼  ',
                     '  1D100抽出中 ~ ｜  ',
                     '  1D100抽出中 ~ ／  ']
      p_bar = Qw.QProgressDialog(
          rollTheDice[0], None, 0, 100, self)  # type: ignore
      p_bar.setWindowModality(Qc.Qt.WindowModality.WindowModal)
      p_bar.setWindowTitle('ガチャ抽選')
      p_bar.show()
      p_barValue = 15
      for p in range(p_barValue):
        p_bar.setValue(int(p / p_barValue * 101))
        if p % 3 == 0:
          p_bar.setLabelText(rollTheDice[p // 3 % len(rollTheDice)])
        Qt.QTest.qWait(20)
      p_bar.close()
      if self.playerTurn:
        tempText += f'相手は 成功値({vfd.attacks[self.enemyAttackCtrl].successRate}) の攻撃を準備している。\n\n'
        tempText += self.MyAttack()
        if self.rbId_attack == 4:
          vfd.playerStatus.Bullets -= 1
      else:
        tempText += 'あなたのターンです。\n\n'
        tempText += self.EnemyAttack()
        if self.enemyAttackCtrl == 4:
          vfd.enemyStatus.Bullets -= 1
        self.enemyAttackCtrl = randint(1, len(vfd.attacks)) - 1  # 敵の行動のリセット。
        while self.rbId_attack == 4 and vfd.enemyStatus.Bullets == 0:
          self.enemyAttackCtrl = randint(1, len(vfd.attacks)) - 1  # 敵の行動のリセット。
        self.enemyDefenceCtrl = randint(1, len(vfd.defences)) - 1
      self.playerTurn = not self.playerTurn

    tempText += self.tb_log.toPlainText()
    self.tb_log.setPlainText(tempText)

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
