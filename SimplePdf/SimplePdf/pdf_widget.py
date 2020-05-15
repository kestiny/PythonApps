#-*-coding:utf-8-*-
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUi
from pdfoperator import pdf_operator, pdf_printer

class PdfWidget(QtWidgets.QDialog):
    """docstring for PdfWidget"""
    count_range = 0
    contextMenu = None
    def __init__(self, parent = None):
        super(PdfWidget, self).__init__(parent)
        loadUi("pdf_widget.ui", self)
        addAction = QtWidgets.QAction("添加文件", self);
        addAction.triggered.connect(self.add_file_to_merge)
        delAction = QtWidgets.QAction("删除文件", self);
        delAction.triggered.connect(self.del_file_to_merge)
        self.contextMenu = QtWidgets.QMenu()
        self.contextMenu.addAction(addAction);
        self.contextMenu.addAction(delAction);
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showListMenu)
        self.listWidget_html.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget_html.customContextMenuRequested.connect(self.showListMenuHtml)
        self.pushButton_split.clicked.connect(self.split_pdf)
        self.pushButton.clicked.connect(self.add_file)
        self.pushButton_merge.clicked.connect(self.merge_file)
        self.pushButton_merge_html.clicked.connect(self.html_to_pdf)

    def split_pdf(self):
        file_path = self.lineEdit.text()
        if os.path.exists(file_path):
            split_range = self.textEdit.toPlainText()
            print(split_range)
            split_range = split_range.replace("，", ",")
            print(type(split_range), split_range)
            pdf_operator.PdfOperator().split(file_path, split_range.split(","))
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:" + os.path.dirname(file_path)))
        
    def add_file(self):
        file_path,_ = QtWidgets.QFileDialog.getOpenFileName(self, "选择分割文件", "/", "PDF(*.pdf)")
        self.lineEdit.setText(file_path)
        self.textEdit.clear()

    def merge_file(self):
        files = []
        for item in [self.listWidget.item(row) for row in range(self.listWidget.count())]:
            files.append(item.text())
        output_path = pdf_operator.PdfOperator().merge(files)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:" + os.path.dirname(output_path)))

    def showListMenu(self, point):
        self.contextMenu.exec(QtGui.QCursor.pos())

    def showListMenuHtml(self, point):
        self.contextMenu.exec(QtGui.QCursor.pos())

    def add_file_to_merge(self):
        if self.tabWidget.currentIndex() == 1:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "选择要合并的文件", "/", "PDF(*.pdf)")
            for file in file_path:
                self.listWidget.addItem(file)
        if self.tabWidget.currentIndex() == 2:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "选择要转换的Html文件", "/", "Html(*.Html)")
            for file in file_path:
                self.listWidget_html.addItem(file)

    def del_file_to_merge(self):
        if self.tabWidget.currentIndex() == 1:
            self.listWidget.takeItem(self.listWidget.currentRow())
        if self.tabWidget.currentIndex() == 2:
            self.listWidget_html.takeItem(self.listWidget_html.currentRow())

    def html_to_pdf(self):
        files = []
        for item in [self.listWidget_html.item(row) for row in range(self.listWidget_html.count())]:
            files.append(item.text())
        pdf_printer.pdf_printer().html_to_pdf(files)
        