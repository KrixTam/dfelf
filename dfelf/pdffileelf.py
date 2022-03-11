from PIL import Image
from shutil import copyfile
from PyPDF2.pdf import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from ni.config import Config
from dfelf import DataFileElf
from dfelf.commons import logger
from moment import moment


class PDFFileElf(DataFileElf):

    def __init__(self, output_dir=None, output_flag=True):
        super().__init__(output_dir, output_flag)

    def init_config(self):
        self._config = Config({
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
                if self._output_flag:
                    get_path = self.get_output_path
                else:
                    get_path = self.get_log_path
                for i in range(len(kwargs['pages'])):
                    output_filename = output_filename_prefix + '_' + str(output_pages[i]) + '.' + image_format
                    kwargs['pages'][i].save(get_path(output_filename), formats[image_format])
            else:
                if task_key == 'reorganize':
                    output_filename = self._config[task_key]['output']
                    ot_filename = self.get_log_path(output_filename)
                    output_stream = open(ot_filename, 'wb')
                    kwargs['pdf_writer'].write(output_stream)
                    output_stream.close()
                    if self._output_flag:
                        output_filename_real = self.get_output_path(output_filename)
                        copyfile(ot_filename, output_filename_real)

    def reorganize(self, input_obj: PdfFileReader = None, **kwargs):
        task_key = 'reorganize'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            if input_obj is None:
                input_stream = open(input_filename, 'rb')
                pdf_file = PdfFileReader(input_stream)
            else:
                pdf_file = input_obj
            pages = self._config[task_key]['pages']
            output = PdfFileWriter()
            pdf_pages_len = pdf_file.getNumPages()
            ori_pages = range(1, pdf_pages_len + 1)
            for page in pages:
                if page in ori_pages:
                    output.addPage(pdf_file.getPage(page - 1))
                else:
                    logger.warning([4000, input_filename, page])
            self.to_output(task_key, pdf_writer=output)
            pdf_file.stream.close()
            # 从log目录中生成返回对象
            output_filename_res = self.get_log_path(self._config[task_key]['output'])
            input_stream_res = open(output_filename_res, 'rb')
            res = PdfFileReader(input_stream_res)
            return res

    def image2pdf(self, input_obj: list = None, **kwargs):
        task_key = 'image2pdf'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            if input_obj is None:
                image_filenames = self._config[task_key]['images']
                num_filenames = len(image_filenames)
                if num_filenames > 0:
                    image_0 = Image.open(image_filenames[0]).convert('RGB')
                    image_list = []
                    for i in range(1, num_filenames):
                        image = Image.open(image_filenames[i]).convert('RGB')
                        image_list.append(image)
                    self.to_output(task_key, first_image=image_0, append_images=image_list)
                    # 从log目录中生成返回对象
                    output_filename = self.get_log_path(self._config[task_key]['output'])
                    input_stream = open(output_filename, 'rb')
                    pdf_file = PdfFileReader(input_stream)
                    return pdf_file
                else:
                    logger.warning([4001])
                    return None
            else:
                num_filenames = len(input_obj)
                if num_filenames > 0:
                    image_0 = input_obj[0].copy().convert('RGB')
                    image_list = []
                    for i in range(1, num_filenames):
                        image = input_obj[i].copy().convert('RGB')
                        image_list.append(image)
                    self.to_output(task_key, first_image=image_0, append_images=image_list)
                    # 从log目录中生成返回对象
                    output_filename = self.get_log_path(self._config[task_key]['output'])
                    input_stream = open(output_filename, 'rb')
                    pdf_file = PdfFileReader(input_stream)
                    return pdf_file
                else:
                    logger.warning([4001])
                    return None

    def to_image(self, input_obj: PdfFileReader = None, **kwargs):
        task_key = '2image'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            if input_obj is None:
                input_filename = self._config[task_key]['input']
                input_stream = open(input_filename, 'rb')
                pdf_file = PdfFileReader(input_stream, strict=False)
            else:
                pdf_file = input_obj
            reorganize_config = {
                'output': 'tmp_' + str(moment().unix_timestamp()) + '.pdf',
                'pages': self._config[task_key]['pages']
            }
            output_flag = self._output_flag
            self._output_flag = False
            self.reorganize(pdf_file, **reorganize_config)
            self._output_flag = output_flag
            pages = convert_from_path(self.get_log_path(reorganize_config['output']), self._config[task_key]['dpi'])
            self.to_output(task_key, pages=pages)
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
