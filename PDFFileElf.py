# coding: utf-8


from DataFileElf import DataFileElf
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
import logging
import os


class PDFFileElf(DataFileElf):

    def __init__(self, cfg_filename=None):
        super().__init__(cfg_filename)

    def splitPDF(self, *args):
        input_filename = ''
        output_filename = ''
        pages = []
        if 3 == len(args):
            input_filename = args[0]
            output_filename = args[1]
            pages = args[2]
            if isinstance(input_filename, str):
                if isinstance(output_filename, str):
                    if isinstance(pages, list):
                        pass
                    else:
                        TypeError('Parameter pages should be list.')
                else:
                    TypeError('Parameter output_filename should be string.')
            else:
                TypeError('Parameter input_filename should be string.')
        else:
            if self._config is None:
                pass
            else:
                pages = self._config['concat']
                input_filename = self._config['input']
                output_filename = self._config['output']
        if len(pages) > 0:
            output = PdfFileWriter()
            input_stream = open(os.path.join(self._cwd, input_filename), "rb")
            pdf_file = PdfFileReader(input_stream)
            pdf_pages_len = pdf_file.getNumPages()
            ori_pages = range(1, pdf_pages_len + 1)
            for page in pages:
                if page in ori_pages:
                    output.addPage(pdf_file.getPage(page - 1))
                else:
                    logging.warning('Page ' + str(page) + ' is not found in PDF file "' + input_filename + '".')
            output_stream = open(os.path.join(self._cwd, output_filename), "wb")
            output.write(output_stream)
            output_stream.close()
            input_stream.close()
        else:
            logging.warning('Pages for split are not set.')
