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

    # ゲーム終了後にボタンが押されたとき、処理が行われないようにするための定義
    self.GameStart = True

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
    self.btn_run.setGeometry(120, vfd.mainTextBoxSize[1] - 100, 250, 60)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # メインテキストボックス
    self.mainLog = Qw.QTextEdit('', self)
    self.mainLog.setGeometry(
        vfd.mainTextBoxPos[0], vfd.mainTextBoxPos[1], vfd.mainTextBoxSize[0], vfd.mainTextBoxSize[1])
    self.mainLog.setReadOnly(True)
    if self.playerTurn:
      self.mainLog.setPlainText(
          f'あなたのターンです。\n\n{vfd.enemyStatus.name} が現れた！\n戦闘技能と防御技能を選択して戦いに備えよう！\n' + vfd.fastSecondTXT)
    else:
      self.mainLog.setPlainText(
          f'相手は 成功値({vfd.attacks[self.enemyAttackCtrl].successRate}) の攻撃を準備している。\n\n {vfd.enemyStatus.name} が現れた！\n戦闘技能と防御技能を選択して戦いに備えよう！\n' + vfd.fastSecondTXT)

    # プレイヤーステータス表示テキストボックス
    self.playerStatus_TB = Qw.QTextEdit('', self)
    self.playerStatus_TB.setGeometry(
        vfd.P_statusTextBoxPos[0], vfd.P_statusTextBoxPos[1], vfd.statusTextBoxSize[0], vfd.statusTextBoxSize[1])
    self.playerStatus_TB.setReadOnly(True)
    self.playerStatus_TB.setPlainText(f'\
{vfd.playerStatus.name} のステータス\n\
  STR   = {vfd.playerStatus.state_STR}\n\
  CON   = {vfd.playerStatus.state_CON}\n\
  SiZ   = {vfd.playerStatus.state_SIZ}\n\
  DEX   = {vfd.playerStatus.state_DEX}\n\
  APP   = {vfd.playerStatus.state_APP}\n\
  INT   = {vfd.playerStatus.state_INT}\n\
  POW   = {vfd.playerStatus.state_POW}\n\
  EDU   = {vfd.playerStatus.state_EDU}\n\
  HP    = {vfd.playerStatus.state_HP}\n\
bullets = {vfd.playerStatus.bullets}')

    # 敵ステータス表示テキストボックス
    self.enemyStatus_TB = Qw.QTextEdit('', self)
    self.enemyStatus_TB.setGeometry(
        vfd.E_statusTextBoxPos[0], vfd.E_statusTextBoxPos[1], vfd.statusTextBoxSize[0], vfd.statusTextBoxSize[1])
    self.enemyStatus_TB.setReadOnly(True)
    self.enemyStatus_TB.setPlainText(f'\
{vfd.enemyStatus.name} のステータス\n\
  STR   = {vfd.enemyStatus.state_STR}\n\
  CON   = {vfd.enemyStatus.state_CON}\n\
  SiZ   = {vfd.enemyStatus.state_SIZ}\n\
  DEX   = {vfd.enemyStatus.state_DEX}\n\
  APP   = {vfd.enemyStatus.state_APP}\n\
  INT   = {vfd.enemyStatus.state_INT}\n\
  POW   = {vfd.enemyStatus.state_POW}\n\
  EDU   = {vfd.enemyStatus.state_EDU}\n\
  HP    = {vfd.enemyStatus.state_HP}\n\
bullets = {vfd.enemyStatus.bullets}')

    # ステータスバー
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage('～プログラム起動中～')

  def StatusUpdate(self, status: vfd.Status):
    tempText = f'\
{status.name} のステータス\n\
  STR   = {status.state_STR}\n\
  CON   = {status.state_CON}\n\
  SiZ   = {status.state_SIZ}\n\
  DEX   = {status.state_DEX}\n\
  APP   = {status.state_APP}\n\
  INT   = {status.state_INT}\n\
  POW   = {status.state_POW}\n\
  EDU   = {status.state_EDU}\n\
  HP    = {status.state_HP}\n\
bullets = {status.bullets}'
    return (tempText)

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
        vfd.playerStatus.state_HP -= 1
        self.playerStatus_TB.setPlainText(self.StatusUpdate(vfd.playerStatus))
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
          if self.enemyDefenceCtrl == 2:
            counterDamageTemp = vfd.DiceRoll(1, 4, 0)
            rollResultTXT += f'攻撃は敵に命中した！({mainDamageTemp}ダメージ)\n'
            rollResultTXT += vfd.enemyAvoid[self.enemyDefenceCtrl] + \
                f'1D4 => {counterDamageTemp}ダメージ\n'
            vfd.playerStatus.state_HP -= counterDamageTemp
            self.playerStatus_TB.setPlainText(
                self.StatusUpdate(vfd.playerStatus))
          else:
            mainDamageTemp = 0
            rollResultTXT += vfd.enemyAvoid[self.enemyDefenceCtrl]
        else:
          rollResultTXT += f'敵：{vfd.defences[self.enemyDefenceCtrl].name}（{successRateDefTemp[self.enemyDefenceCtrl]}） ＜ {enemyDiceResult}　失敗\n'
          if self.enemyDefenceCtrl == 1:
            mainDamageTemp -= floor(5 - enemyDiceResult / 20)
          rollResultTXT += f'攻撃は敵に命中した！({mainDamageTemp}ダメージ)\n'
      vfd.enemyStatus.state_HP -= mainDamageTemp
      self.enemyStatus_TB.setPlainText(self.StatusUpdate(vfd.enemyStatus))
    rollResultTXT += "\n\n"
    if vfd.enemyStatus.state_HP <= 0:
      self.GameStart = False
      self.enemyStatus_TB.setPlainText(
          'Died\n\n' + self.StatusUpdate(vfd.enemyStatus))
      gameEndTXT = '敵を打ち倒しました！あなたの勝ちです。\n'
      gameEndTXT += 'ゲームを再起動するか、右上のバツ印からゲームを終了してください。\n\n'
      gameEndTXT += rollResultTXT
      return gameEndTXT
    elif vfd.playerStatus.state_HP <= 0:
      self.GameStart = False
      self.playerStatus_TB.setPlainText(
          'Died\n\n' + self.StatusUpdate(vfd.enemyStatus))
      gameEndTXT = 'あなたはしんでしまいました...あなたの負けです。\n'
      gameEndTXT += 'ゲームを再起動するか、右上のバツ印からゲームを終了してください。\n\n'
      gameEndTXT += rollResultTXT
      return gameEndTXT
    else:
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
        vfd.enemyStatus.state_HP -= 1
        self.enemyStatus_TB.setPlainText(self.StatusUpdate(vfd.enemyStatus))
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
          if self.rbId_defence == 2:
            counterDamageTemp = vfd.DiceRoll(1, 4, 0)
            rollResultTXT += f'敵の攻撃を受けてしまった！({mainDamageTemp}ダメージ)\n'
            rollResultTXT += vfd.playerAvoid[self.rbId_defence] + \
                f'1D4 => {counterDamageTemp}ダメージ\n'
            vfd.enemyStatus.state_HP -= counterDamageTemp
            self.enemyStatus_TB.setPlainText(self.StatusUpdate(vfd.enemyStatus))
          else:
            mainDamageTemp = 0
            rollResultTXT += vfd.playerAvoid[self.rbId_defence]
        else:
          rollResultTXT += f'自分：{vfd.defences[self.rbId_defence].name}（{successRateDefTemp[self.rbId_defence]}） ＜ {myDiceResult}　失敗\n'
          if self.rbId_defence == 1:
            mainDamageTemp -= floor(5 - myDiceResult / 20)
          rollResultTXT += f'敵の攻撃を受けてしまった！({mainDamageTemp}ダメージ)\n'
      vfd.playerStatus.state_HP -= mainDamageTemp
      self.playerStatus_TB.setPlainText(self.StatusUpdate(vfd.playerStatus))
    rollResultTXT += "\n\n"
    if vfd.playerStatus.state_HP <= 0:
      self.GameStart = False
      self.playerStatus_TB.setPlainText(
          'Died\n\n' + self.StatusUpdate(vfd.enemyStatus))
      gameEndTXT = 'あなたはしんでしまいました...あなたの負けです。\n'
      gameEndTXT += 'ゲームを再起動するか、右上のバツ印からゲームを終了してください。\n\n'
      gameEndTXT += rollResultTXT
      return gameEndTXT
    elif vfd.enemyStatus.state_HP <= 0:
      self.GameStart = False
      self.enemyStatus_TB.setPlainText(
          'Died\n\n' + self.StatusUpdate(vfd.enemyStatus))
      gameEndTXT = '敵を打ち倒しました！あなたの勝ちです。\n'
      gameEndTXT += 'ゲームを再起動するか、右上のバツ印からゲームを終了してください。\n\n'
      gameEndTXT += rollResultTXT
      return gameEndTXT
    else:
      return rollResultTXT

  # 「実行」ボタンの押下処理
  def btn_run_clicked(self):

    if self.GameStart:
      # 一時保存用のテキストの初期化
      tempText = ''

      # 正常に動作したかの確認用
      normalAct = False

      if self.playerTurn:
        if self.rbId_attack == 4 and vfd.playerStatus.bullets == 0:
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
        p_barValue = 25
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
            vfd.playerStatus.bullets -= 1
            self.playerStatus_TB.setPlainText(
                self.StatusUpdate(vfd.playerStatus))
        else:
          tempText += 'あなたのターンです。\n\n'
          tempText += self.EnemyAttack()
          if self.enemyAttackCtrl == 4:
            vfd.enemyStatus.bullets -= 1
            self.enemyStatus_TB.setPlainText(
                self.StatusUpdate(vfd.enemyStatus))
          self.enemyAttackCtrl = randint(1, len(vfd.attacks)) - 1  # 敵の行動のリセット。
          while self.rbId_attack == 4 and vfd.enemyStatus.bullets == 0:
            self.enemyAttackCtrl = randint(
                1, len(vfd.attacks)) - 1  # 敵の行動のリセット。
          self.enemyDefenceCtrl = randint(1, len(vfd.defences)) - 1
        self.playerTurn = not self.playerTurn

      tempText += self.mainLog.toPlainText()
      self.mainLog.setPlainText(tempText)

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
