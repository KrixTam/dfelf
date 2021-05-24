# coding: utf-8


from DataFileElf import DataFileElf
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
import logging
from config import config


class PDFFileElf(DataFileElf):

    def __init__(self):
        super().__init__()

    def init_config(self):
        self._config = config({
            'name': 'PDFFileElf',
            'default': {
                'input': 'input_filename',
                'output': 'output_filename',
                'concat': []
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'input': {'type': 'string'},
                    'output': {'type': 'string'},
                    'concat': {
                        'type': 'array',
                        'items': {'type': 'number'}
                    }
                }
            }
        })

    def reorganize(self, default_output=True, **kwargs):
        self.set_config(**kwargs)
        input_filename = self._config['input']
        output_filename = self._config['output']
        pages = self._config['concat']
        if len(pages) > 0:
            output = PdfFileWriter()
            input_stream = open(self.get_filename_with_path(input_filename), "rb")
            pdf_file = PdfFileReader(input_stream)
            pdf_pages_len = pdf_file.getNumPages()
            ori_pages = range(1, pdf_pages_len + 1)
            for page in pages:
                if page in ori_pages:
                    output.addPage(pdf_file.getPage(page - 1))
                else:
                    logging.warning('Page ' + str(page) + ' is not found in PDF file "' + input_filename + '".')
            ot_filename = self.get_filename_with_path(output_filename)
            if default_output:
                ot_filename = self.get_output_path(output_filename)
            output_stream = open(ot_filename, "wb")
            output.write(output_stream)
            output_stream.close()
            input_stream.close()
        else:
            logging.warning('Pages for split are not set.')

    def to_image(self, *args):
        # TODO
        pass
