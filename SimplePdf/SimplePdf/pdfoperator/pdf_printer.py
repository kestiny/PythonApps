#-*-coding:utf-8-*-
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtPrintSupport import *

class pdf_printer(object):
    """docstring for pdf_printer"""
    def __init__(self):
        super(pdf_printer, self).__init__()
        
    def html_to_pdf(self, file_list):
        if len(file_list) <= 0:
            return

        html_printer = QPrinter()
        html_printer.setOutputFormat(QPrinter.PdfFormat)
        doc = QtGui.QTextDocument()
        for file in file_list:
            with open(file, 'rb') as html:
                html_printer.setOutputFileName(file.replace(".html", ".pdf"))
                doc.setHtml(str(html.read()))
                doc.print(html_printer)