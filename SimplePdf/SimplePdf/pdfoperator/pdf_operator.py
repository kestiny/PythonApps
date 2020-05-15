#-*-coding:utf-8-*-
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

class PdfOperator(object):
    """docstring for PdfOperator"""

    def __init__(self):
        super(PdfOperator, self).__init__()

    def split(self, input_file, split_list):
        if not os.path.exists(input_file):
            return
        print(split_list)
        file_name = os.path.basename(input_file)
        file_path = os.path.dirname(input_file)
        pdf = PdfFileReader(input_file, 'rb')
        for iter in split_list:
            rang = iter.split('-')
            pdf_writer = PdfFileWriter()
            for page in range(int(rang[0]), min([int(rang[1]), pdf.getNumPages()])):
                pdf_writer.addPage(pdf.getPage(page))
            
            output = f'{file_path}/{file_name}_{iter}.pdf'
            with open(output, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

    def merge(self, file_list):
        if len(file_list) <= 0:
            return

        pdf_writer = PdfFileWriter()
        for file in file_list:
            pdf = PdfFileReader(file, 'rb')
            for page in range(pdf.getNumPages()):
                pdf_writer.addPage(pdf.getPage(page))

        output = f'{file_list[0]}_merge.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        return output
