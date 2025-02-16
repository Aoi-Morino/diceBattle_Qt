import sys
import random as r
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt
import varFunc_def as vfd

# MainWindowクラス定義 ####
class MainWindow(Qw.QMainWindow):

  # *MainWIndow
  def __init__(self):
    super().__init__()

    # ウィンドウサイズの固定
    self.setFixedSize(vfd.mainWindowSize[0], vfd.mainWindowSize[1])

    # ウィンドウの位置をスクリーン中央に設定
    rect = Qc.QRect()
    rect.setSize(Qc.QSize(vfd.mainWindowSize[0], vfd.mainWindowSize[1]))
    rect.moveCenter(app.primaryScreen().availableGeometry().center())
    self.setGeometry(rect)

    # 「実行」ボタンの生成と設定
    self.btn_run = Qw.QPushButton('実行', self)
    self.btn_run.setGeometry(10, 10, 100, 20)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('', self)
    self.tb_log.setGeometry(10, 40, 620, 420)
    self.tb_log.setReadOnly(True)
    self.tb_log.setPlaceholderText('(ここに実行ログを表示します)')

    # ステータスバー
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)
    self.sb_status.showMessage('～プログラム起動中～')

  # 「実行」ボタンの押下処理
  def btn_run_clicked(self):

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

    # テキストボックスの表示を更新
    log = f'{vfd.Dice_1D100()}\n'
    log += self.tb_log.toPlainText()
    self.tb_log.setPlainText(log)

# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())
