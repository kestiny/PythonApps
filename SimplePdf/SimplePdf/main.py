#-*-coding:utf-8-*-
import sys
from PyQt5 import QtWidgets
from pdf_widget import PdfWidget

app = QtWidgets.QApplication(sys.argv)
widget = PdfWidget()
widget.show()
sys.exit(app.exec())
