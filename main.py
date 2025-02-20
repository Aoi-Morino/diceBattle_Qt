import sys
import random as r
import math as m
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt
import varFunc_def as vfd

# * MainWindowクラス定義
class MainWindow(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    # 事前に敵の初めの行動を一度決めておく
    self.enemyAttackCtrl = r.randint(1, len(vfd.attacks)) - 1
    self.enemyDefenceCtrl = r.randint(1, len(vfd.defences)) - 1

    # 戦闘・守備技能未選択時のラジオボタンのIDの設定
    self.rbId_attack = len(vfd.attacks)
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
    self.btn_run = Qw.QPushButton('実行', self)
    self.btn_run.setGeometry(vfd.textBoxPos[0], vfd.textBoxPos[1], 100, 20)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('', self)
    self.tb_log.setGeometry(
        vfd.textBoxPos[0], vfd.textBoxPos[1] + 30, vfd.textBoxSize[0], vfd.textBoxSize[1])
    self.tb_log.setReadOnly(True)
    self.tb_log.setPlainText(
        f'相手は {vfd.attacks[self.enemyAttackCtrl].name} の準備をしている。\n {vfd.enemyName} が現れた！\n戦闘技能と防御技能を選択して戦いに備えよう！\n' + vfd.fastSecondTXT)

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
        TempTXT += ' | 速度：先行'
      else:
        TempTXT += ' | 速度：順行'
      if vfd.attacks[self.rbId_attack].indirect:
        TempTXT += ' | 距離：遠距離'
      else:
        TempTXT += ' | 距離：近距離'
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

  # こちらの攻撃の処理
  def MyAttack(self):
    success = False
    myDiceResult = vfd.DiceRoll(1, 100, 0)
    if vfd.attacks[self.rbId_attack].successRate >= myDiceResult:
      success = True
      if 5 >= myDiceResult:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ≧ {myDiceResult}　クリティカル（決定的成功）\n攻撃力二倍！\n'
        damageTemp = vfd.DiceRoll(
            vfd.attacks[self.rbId_attack].dice * 2, vfd.attacks[self.rbId_attack].damage, 0)
        rollResultTXT += f'2D{vfd.attacks[self.rbId_attack].damage} => {damageTemp}\n'
      else:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ≧ {myDiceResult}　成功\n'
        damageTemp = vfd.DiceRoll(
            vfd.attacks[self.rbId_attack].dice, vfd.attacks[self.rbId_attack].damage, 0)
        rollResultTXT += f'1D{vfd.attacks[self.rbId_attack].damage} => {damageTemp}\n'
    else:
      if 95 >= myDiceResult:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ＜ {myDiceResult}　失敗\n'
      else:
        rollResultTXT = f'自分：{vfd.attacks[self.rbId_attack].name}（{vfd.attacks[self.rbId_attack].successRate}） ＜ {myDiceResult}　ファンブル（致命的失敗）\n転んで1ダメージ...\n'

    # ここから敵の処理
    if success:
      successRateDefTemp = [myDiceResult + 20,
                            (5 - damageTemp) * 20,
                            60]
      for i in range(len(successRateDefTemp)):
        if successRateDefTemp[i] <= 0:
          successRateDefTemp[i] = 0
        elif successRateDefTemp[i] >= 100:
          successRateDefTemp[i] = 100
      enemyDiceResult = vfd.DiceRoll(1, 100, 0)
      if successRateDefTemp[self.enemyDefenceCtrl] >= enemyDiceResult:
        rollResultTXT += f'敵：{vfd.defences[self.enemyDefenceCtrl].name}（{successRateDefTemp[self.enemyDefenceCtrl]}） ≧ {enemyDiceResult}　成功\n'
        rollResultTXT += vfd.enemyAvoid[self.enemyDefenceCtrl]
      else:
        rollResultTXT += f'敵：{vfd.defences[self.enemyDefenceCtrl].name}（{successRateDefTemp[self.enemyDefenceCtrl]}） ＜ {enemyDiceResult}　失敗\n'
        if self.enemyDefenceCtrl == 1:
          damageTemp -= m.floor(5 - enemyDiceResult / 20)
        rollResultTXT += f'攻撃は敵に命中した！({damageTemp}ダメージ)\n'
    rollResultTXT += "\n"
    return rollResultTXT

  # 守備ダイスの処理
  def DefenceDice(self):
    myDiceResult = vfd.DiceRoll(1, 100, 0)
    if self.successRateDefTemp[self.rbId_defence] >= myDiceResult:
      if 5 >= myDiceResult:
        rollResultTXT = f'{vfd.defences[self.rbId_defence].name}（{vfd.defences[self.rbId_defence].srTest}） ≧ {myDiceResult}　クリティカル（決定的成功）\n'
      else:
        rollResultTXT = f'{vfd.defences[self.rbId_defence].name}（{vfd.defences[self.rbId_defence].srTest}） ≧ {myDiceResult}　成功\n'
    else:
      if 95 >= myDiceResult:
        rollResultTXT = f'{vfd.defences[self.rbId_defence].name}（{vfd.defences[self.rbId_defence].srTest}） ＜ {myDiceResult}　失敗\n'
      else:
        rollResultTXT = f'{vfd.defences[self.rbId_defence].name}（{vfd.defences[self.rbId_defence].srTest}） ＜ {myDiceResult}　ファンブル（致命的失敗）\n'
    return rollResultTXT

  # 「実行」ボタンの押下処理
  def btn_run_clicked(self):

    # 一時保存用のテキストの初期化
    tempText = ''

    # 正常に動作したかの確認用
    normalAct = True

    if 0 <= self.rbId_attack < len(vfd.attacks):
      pass
    elif self.rbId_attack == len(vfd.attacks):
      tempText += 'error! 戦闘技能が選択されていません。\n'
      normalAct = False
    else:
      tempText += 'error! 戦闘技能が異常な選択です。制作者に報告し、再度選択するか進行が不可能な場合はゲームを再起動してください。\n'
      normalAct = False
    if 0 <= self.rbId_defence < len(vfd.defences):
      pass
    elif self.rbId_defence == len(vfd.defences):
      tempText += 'error! 守備技能が選択されていません。\n'
      normalAct = False
    else:
      tempText += 'error! 守備技能が異常な選択です。制作者に報告し、再度選択するか進行が不可能な場合はゲームを再起動してください。\n'
      normalAct = False

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
      subTempText = self.MyAttack()

      # self.successRateDefTemp = [vfd.defences[0].srTest,
      #                            vfd.defences[1].srTest,
      #                            vfd.defences[2].srTest]
      # self.myDiceResult = vfd.DiceRoll(1, 100, 0)
      # tempText += self.DefenceDice()

      # 敵の行動のリセット。
      self.enemyAttackCtrl = r.randint(1, len(vfd.attacks)) - 1
      self.enemyDefenceCtrl = r.randint(1, len(vfd.defences)) - 1
      tempText += f'相手は {vfd.attacks[self.enemyAttackCtrl].name} の準備をしている。\n'

    tempText += subTempText
    tempText += self.tb_log.toPlainText()
    self.tb_log.setPlainText(tempText)

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
