# coding: utf-8

from DataFileElf import DataFileElf
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
import logging
from config import config
from PIL import Image


class PDFFileElf(DataFileElf):

    def __init__(self):
        super().__init__()

    def init_config(self):
        self._config = config({
            'name': 'PDFFileElf',
            'default': {
                'reorganize': {
                    'input': 'input_filename',
                    'output': 'output_filename',
                    'pages': []
                },
                'image2pdf': {
                    'images': [],
                    'output': 'output_filename'
                },
                '2image': {}
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'reorganize': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'pages': {
                                'type': 'array',
                                'items': {'type': 'number'}
                            }
                        }
                    },
                    'image2pdf': {
                        'type': 'object',
                        'properties': {
                            'images': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'output': {'type': 'string'}
                        }
                    },
                    '2image': {
                        'type': 'object'
                    }
                }
            }
        })

    def reorganize(self, **kwargs):
        new_kwargs = {
            'reorganize': kwargs
        }
        self.set_config(**new_kwargs)
        input_filename = self._config['reorganize']['input']
        output_filename = self._config['reorganize']['output']
        pages = self._config['reorganize']['pages']
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
                    logging.warning('PDF文件"' + input_filename + '"中不存在第' + str(page) + '的内容，请检查PDF原文档的内容正确性或者配置正确性。')
            ot_filename = self.get_filename_with_path(output_filename)
            output_stream = open(ot_filename, "wb")
            output.write(output_stream)
            output_stream.close()
            input_stream.close()
        else:
            logging.warning('"concat"没有设置，请设置后重试。')

    def image2pdf(self, **kwargs):
        new_kwargs = {
            'image2pdf': kwargs
        }
        self.set_config(**new_kwargs)
        image_filenames = self._config['image2pdf']['images']
        output_filename = self._config['image2pdf']['output']
        num_filenames = len(image_filenames)
        if num_filenames > 0:
            image_0 = Image.open(self.get_filename_with_path(image_filenames[0])).convert('RGB')
            image_list = []
            for i in range(1, num_filenames):
                image = Image.open(self.get_filename_with_path(image_filenames[i])).convert('RGB')
                image_list.append(image)
            image_0.save(self.get_output_path(output_filename), save_all=True, append_images=image_list)
        else:
            logging.warning('"from_images"没有设置，请设置后重试。')

    def to_image(self, *args):
        # TODO
        pass
