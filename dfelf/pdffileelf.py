# coding: utf-8

from .datafileelf import DataFileElf
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
import logging
from config import config
from PIL import Image
from pdf2image import convert_from_bytes
from io import BytesIO
from shutil import copyfile


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
                    'pages': [1]
                },
                'image2pdf': {
                    'images': [],
                    'output': 'output_filename'
                },
                '2image': {
                    'input': 'input_filename',
                    'output': 'output_filename_prefix',
                    'format': 'png',
                    'dpi': 200,
                    'pages': [1]
                }
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
                                'items': {'type': 'integer'},
                                'minItems': 1
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
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'format': {
                                "type": "string",
                                "enum": ['png', 'jpg', 'tif']
                            },
                            'dpi': {'type': 'integer'},
                            'pages': {
                                'type': 'array',
                                'items': {'type': 'integer'},
                                'minItems': 1
                            }
                        }
                    }
                }
            }
        })

    def to_output(self, task_key, **kwargs):
        if task_key == 'image2pdf':
            output_filename = self.get_log_path(self._config[task_key]['output'])
            kwargs['first_image'].save(output_filename, save_all=True, append_images=kwargs['append_images'])
            if self._output_flag:
                output_filename_real = self.get_output_path(self._config[task_key]['output'])
                copyfile(output_filename, output_filename_real)
        else:
            if task_key == '2image':
                formats = {
                    'png': 'PNG',
                    'jpg': 'JPEG',
                    'tif': 'TIFF'
                }
                output_filename_prefix = self._config[task_key]['output']
                image_format = self._config[task_key]['format']
                output_pages = self._config[task_key]['pages']
                dpi = self._config[task_key]['dpi']
                for page_index in output_pages:
                    memory_output = PdfFileWriter()
                    memory_output.addPage(kwargs['pdf'].getPage(page_index - 1))
                    output_stream = BytesIO()
                    memory_output.write(output_stream)
                    pages = convert_from_bytes(output_stream.getvalue(), dpi)
                    output_filename = output_filename_prefix + '_' + str(page_index) + '.' + image_format
                    pages[0].save(self.get_log_path(output_filename), formats[image_format])
                if self._output_flag:
                    for page_index in output_pages:
                        output_filename = output_filename_prefix + '_' + str(page_index) + '.' + image_format
                        src_filename = self.get_log_path(output_filename)
                        dis_filename = self.get_output_path(output_filename)
                        copyfile(src_filename, dis_filename)
            else:
                if task_key == 'reorganize':
                    output_filename = self._config[task_key]['output']
                    ot_filename = self.get_log_path(output_filename)
                    output_stream = open(ot_filename, "wb")
                    kwargs['pdf_writer'].write(output_stream)
                    output_stream.close()
                    if self._output_flag:
                        output_filename_real = self.get_output_path(output_filename)
                        copyfile(ot_filename, output_filename_real)

    def reorganize(self, **kwargs):
        task_key = 'reorganize'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            pages = self._config[task_key]['pages']
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
            self.to_output(task_key, pdf_writer=output)
            input_stream.close()
            # 从log目录中生成返回对象
            output_filename_res = self.get_log_path(self._config[task_key]['output'])
            input_stream_res = open(output_filename_res, "rb")
            res = PdfFileReader(input_stream_res)
            return res

    def image2pdf(self, **kwargs):
        task_key = 'image2pdf'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            image_filenames = self._config[task_key]['images']
            num_filenames = len(image_filenames)
            if num_filenames > 0:
                image_0 = Image.open(self.get_filename_with_path(image_filenames[0])).convert('RGB')
                image_list = []
                for i in range(1, num_filenames):
                    image = Image.open(self.get_filename_with_path(image_filenames[i])).convert('RGB')
                    image_list.append(image)
                self.to_output(task_key, first_image=image_0, append_images=image_list)
                # 从log目录中生成返回对象
                output_filename = self.get_log_path(self._config[task_key]['output'])
                input_stream = open(output_filename, "rb")
                pdf_file = PdfFileReader(input_stream)
                return pdf_file
            else:
                logging.warning('"from_images"没有设置，请设置后重试。')
                return None

    def to_image(self, **kwargs):
        task_key = '2image'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            input_stream = open(self.get_filename_with_path(input_filename), "rb")
            pdf_file = PdfFileReader(input_stream, strict=False)
            self.to_output(task_key, pdf=pdf_file)
            input_stream.close()
            output_filename_prefix = self._config[task_key]['output']
            image_format = self._config[task_key]['format']
            output_pages = self._config[task_key]['pages']
            res = []
            if self._output_flag:
                for page_index in output_pages:
                    output_filename = output_filename_prefix + '_' + str(page_index) + '.' + image_format
                    res.append(self.get_output_path(output_filename))
            else:
                for page_index in output_pages:
                    output_filename = output_filename_prefix + '_' + str(page_index) + '.' + image_format
                    res.append(self.get_log_path(output_filename))
            return res
