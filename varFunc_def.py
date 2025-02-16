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
