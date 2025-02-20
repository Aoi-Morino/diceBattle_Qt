import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt
import varFunc_def as vfd

# * MainWindowクラス定義
class MainWindow(Qw.QMainWindow):

  def __init__(self):
    super().__init__()

    # 戦闘技能未選択時のラジオボタンのIDの設定
    self.rbId = len(vfd.attacks)

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
    selectTXT = Qw.QLabel('どう攻撃する？')  # 質問を表示する
    mainLayout.addWidget(selectTXT)

    # ラジオボタンを格納する画面表示上のコンテナ
    rbLayout = Qw.QHBoxLayout()  # 要素を水平配置
    rbLayout.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft)  # 左寄せ
    mainLayout.addLayout(rbLayout)

    # ラジオボタンの生成と設定
    self.attackChoices = Qw.QButtonGroup(self)  # 選択肢のグループ
    for i, attacks in enumerate(vfd.attacks, 1):
      rb = Qw.QRadioButton(self)  # 一つずつラジオボタンを作成する
      rb.setText(attacks.name)
      rbLayout.addWidget(rb)  # レイアウトに追加
      self.attackChoices.addButton(rb, i)  # 選択グループに追加
    # ラジオボタンがクリックされたら下の方のテクストの変化もさせる
    self.attackChoices.buttonClicked.connect(self.RBClicked)
    # 攻撃の説明文
    self.attackExp = Qw.QLabel('')
    mainLayout.addWidget(self.attackExp)  # 空白を挟む
    self.labelTXT = Qw.QLabel('', self)
    mainLayout.addWidget(self.labelTXT)

    # 「実行」ボタンの生成と設定
    self.btn_run = Qw.QPushButton('実行', self)
    self.btn_run.setGeometry(380, 10, 100, 20)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('', self)
    self.tb_log.setGeometry(380, 40, 620, 420)
    self.tb_log.setReadOnly(True)
    self.tb_log.setPlaceholderText('(ここに実行ログを表示します)')

    # ステータスバー
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage('～プログラム起動中～')

  def RBClicked(self):
    self.rbId = self.attackChoices.checkedId() - 1
    if 0 <= self.rbId < len(vfd.attacks):
      TempTXT = f'成功率：{vfd.attacks[self.rbId].successRate}｜ダイス：{vfd.attacks[self.rbId].dice}d{vfd.attacks[self.rbId].damage}'
      if vfd.attacks[self.rbId].fast:
        TempTXT += ' | 速度：先行'
      else:
        TempTXT += ' | 速度：順行'
      if vfd.attacks[self.rbId].indirect:
        TempTXT += ' | 距離：遠距離'
      else:
        TempTXT += ' | 距離：近距離'
    else:
      TempTXT = 'error! 異常な選択です。制作者に報告してください。'
    self.labelTXT.setText(TempTXT)

  def AttackDice(self):
    diceResult = vfd.Dice_1D100()
    if vfd.attacks[self.rbId].successRate >= diceResult:
      if 5 >= diceResult:
        attackDiceResult = f'{vfd.attacks[self.rbId].successRate} ≧ {diceResult}　クリティカル（決定的成功）\n'
      else:
        attackDiceResult = f'{vfd.attacks[self.rbId].successRate} ≧ {diceResult}　成功\n'
    else:
      if 95 >= diceResult:
        attackDiceResult = f'{vfd.attacks[self.rbId].successRate} ＜ {diceResult}　失敗\n'
      else:
        attackDiceResult = f'{vfd.attacks[self.rbId].successRate} ＜ {diceResult}　ファンブル（致命的失敗）\n'
    return attackDiceResult

  # 「実行」ボタンの押下処理
  def btn_run_clicked(self):

    if 0 <= self.rbId < len(vfd.attacks):
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
      p_barValue = 40
      for p in range(p_barValue):
        p_bar.setValue(int(p / p_barValue * 101))
        if p % 3 == 0:
          p_bar.setLabelText(rollTheDice[p // 3 % len(rollTheDice)])
        Qt.QTest.qWait(20)
      p_bar.close()
      attackDiceResult = self.AttackDice()
    elif self.rbId == len(vfd.attacks):
      attackDiceResult = 'error! 戦闘技能が選択されていません。\n'
    else:
      attackDiceResult = 'error! 異常な選択です。制作者に報告し、再度選択するか進行が不可能な場合はゲームを再起動してください。\n'

    attackDiceResult += self.tb_log.toPlainText()
    self.tb_log.setPlainText(attackDiceResult)

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
