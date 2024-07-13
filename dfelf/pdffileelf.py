import os
import pymupdf
from PIL import Image
from ni.config import Config
from dfelf import DataFileElf
from dfelf.commons import logger, is_same_image, random_name
from io import BytesIO

HEX_REG = '{0:0{1}x}'
SERIF = 'serif'
MONO_SPACE = 'monospace'
IGNORE_KEYWORDS = [SERIF, MONO_SPACE]
IMAGE_FORMAT = {
    'png': 'PNG',
    'jpg': 'JPEG',
    'tif': 'TIFF'
}


def check_pages(document: pymupdf.Document, pages: list):
    selected_pages = []
    if len(pages) > 0:
        max_page = document.page_count
        for page in pages:
            if 0 < page <= max_page:
                selected_pages.append(page - 1)
            else:
                logger.error([4003, document.name, max_page, page])
        if len(selected_pages) > 0:
            return selected_pages
        else:
            raise ValueError(logger.error([4004, document.name]))
    else:
        return selected_pages


def open_pdf(file):
    if isinstance(file, pymupdf.Document):
        pdf_file = file
    else:
        if isinstance(file, str):
            pdf_file = pymupdf.open(file)
        else:
            raise TypeError(logger.error([4005, type(file)]))
    return pdf_file


def is_same_pdf(file_1, file_2, ext: str = 'png', dpi: int = 300):
    df_elf = PDFFileElf()
    config = {
        'format': ext,
        'dpi': dpi,
        'pages': []
    }
    pdf_1 = open_pdf(file_1)
    pdf_2 = open_pdf(file_2)
    pages_1 = df_elf.to_image(pdf_1, True, **config)
    pages_2 = df_elf.to_image(pdf_2, True, **config)
    len_pages_1 = len(pages_1)
    len_pages_2 = len(pages_2)
    res = True
    if len_pages_1 == len_pages_2:
        for i in range(len_pages_1):
            if is_same_image(pages_1[i], pages_2[i]):
                pass
            else:
                res = False
    else:
        res = False
    return res


class PDFFileElf(DataFileElf):

    def __init__(self, output_dir=None, output_flag=True):
        super().__init__(output_dir, output_flag)

    def init_config(self):
        self._config = Config({
            'name': 'PDFFileElf',
            'default': {
                'create': {
                    'input': [
                        {
                            'file': 'input_filename_01',
                            'pages': []
                        },
                        {
                            'file': 'input_filename_02',
                            'pages': []
                        },
                    ],
                    'output': 'output_filename'
                },
                'image2pdf': {
                    'images': [],
                    'output': 'output_filename'
                },
                'to_image': {
                    'input': 'input_filename',
                    'output': 'output_filename_prefix',
                    'format': 'png',
                    'dpi': 200,
                    'pages': [1]
                },
                'remove': {
                    'input': 'input_filename',
                    'output': 'output_filename',
                    'pages': [1]
                },
                'extract_images': {
                    'input': 'input_filename',
                    'output': 'output_filename_prefix',
                    'pages': [1]
                },
                'remove_watermark': {
                    'input': 'input_filename',
                    'output': 'output_filename',
                    'keywords': []
                },
                'extract_fonts': {
                    'input': 'input_filename',
                    'output': 'output_directory'
                }
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'create': {
                        'type': 'object',
                        'properties': {
                            'input': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'file': {'type': 'string'},
                                        'pages': {
                                            'type': 'array',
                                            'items': {'type': 'integer'},
                                        }
                                    }
                                },
                                'minItems': 1
                            },
                            'output': {'type': 'string'},
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
                    'to_image': {
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
                                'items': {'type': 'integer'}
                            }
                        }
                    },
                    'remove': {
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
                    'extract_images': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'pages': {
                                'type': 'array',
                                'items': {'type': 'integer'}
                            }
                        }
                    },
                    'remove_watermark': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'keywords': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            }
                        }
                    },
                    'extract_fonts': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'}
                        }
                    }
                }
            }
        })

    def trans_object(self, input_obj, task_key):
        if task_key == 'image2pdf':
            if isinstance(input_obj, str):
                return Image.open(input_obj).convert('RGB')
            else:
                if isinstance(input_obj, Image.Image):
                    return input_obj.copy().convert('RGB')
            raise TypeError(logger.error([4002, task_key, type(input_obj), str, Image.Image]))
        if input_obj is None:
            if self.is_default(task_key):
                return None
            else:
                pdf_file = pymupdf.open(self._config[task_key]['input'])
                return pdf_file
        if isinstance(input_obj, pymupdf.Document):
            temp_file = self.get_log_path('trans_' + random_name() + '.pdf')
            input_obj.save(temp_file)
            pdf_file = pymupdf.open(temp_file)
            return pdf_file
        if isinstance(input_obj, str):
            pdf_file = pymupdf.open(input_obj)
            return pdf_file
        return None

    def to_output(self, task_key, **kwargs):
        if self._output_flag:
            get_path = self.get_output_path
        else:
            get_path = self.get_log_path
        if task_key in ['create', 'remove']:
            output_filename = get_path(self._config[task_key]['output'])
            kwargs['document'].save(output_filename)
        else:
            if task_key in ['to_image', 'extract_images']:
                output_filename = get_path(kwargs['output'])
                kwargs['pixmap'].save(output_filename)
            else:
                if task_key == 'image2pdf':
                    output_filename = get_path(self._config[task_key]['output'])
                    kwargs['first_image'].save(output_filename, save_all=True, append_images=kwargs['append_images'])

    def create(self, input_obj=None, silent: bool = False, **kwargs):
        task_key = 'create'
        self.set_config_by_task_key(task_key, **kwargs)
        pdf_files = []
        if input_obj is None:
            if self.is_default(task_key):
                return None
            else:
                inputs = self._config[task_key]['input']
                for input_info in inputs:
                    pdf_file = self.trans_object(input_info['file'], task_key)
                    selected_pages = check_pages(pdf_file, input_info['pages'])
                    if len(selected_pages) > 0:
                        pdf_file.select(selected_pages)
                    pdf_files.append(pdf_file)
        else:
            input_obj_selected = input_obj
            for input_info in input_obj_selected:
                pdf_file = self.trans_object(input_info['file'], task_key)
                selected_pages = check_pages(pdf_file, input_info['pages'])
                if len(selected_pages) > 0:
                    pdf_file.select(selected_pages)
                pdf_files.append(pdf_file)
        output = pdf_files[0]
        for i in range(1, len(pdf_files)):
            output.insert_pdf(pdf_files[i])
            pdf_files[i].close()
        if silent:
            pass
        else:
            self.to_output(task_key, document=output)
        return output

    def image2pdf(self, input_obj: list = None, silent: bool = False, **kwargs):
        task_key = 'image2pdf'
        self.set_config_by_task_key(task_key, **kwargs)
        if input_obj is None:
            if self.is_default(task_key):
                return None
            else:
                image_filenames = self._config[task_key]['images']
                num_filenames = len(image_filenames)
                if num_filenames > 0:
                    image_0 = self.trans_object(image_filenames[0], task_key)
                    image_list = []
                    for i in range(1, num_filenames):
                        image = self.trans_object(image_filenames[i], task_key)
                        image_list.append(image)
                else:
                    logger.warning([4001])
                    return None
        else:
            num_filenames = len(input_obj)
            if num_filenames > 0:
                image_0 = self.trans_object(input_obj[0], task_key)
                image_list = []
                for i in range(1, num_filenames):
                    image = self.trans_object(input_obj[i], task_key)
                    image_list.append(image)
            else:
                logger.warning([4001])
                return None
        if silent:
            pass
        else:
            self.to_output(task_key, first_image=image_0, append_images=image_list)
        buf = BytesIO()
        image_0.save(buf, format='PDF', save_all=True, append_images=image_list)
        buf.seek(0)
        pdf_file = pymupdf.open(stream=buf, filetype='pdf')
        return pdf_file

    def to_image(self, input_obj: pymupdf.Document = None, silent: bool = False, **kwargs):
        task_key = 'to_image'
        self.set_config_by_task_key(task_key, **kwargs)
        pdf_file = self.trans_object(input_obj, task_key)
        if pdf_file is None:
            return None
        selected_pages = check_pages(pdf_file, self._config[task_key]['pages'])
        output_filename_prefix = self._config[task_key]['output']
        image_format = IMAGE_FORMAT[self._config[task_key]['format']]
        image_dpi = self._config[task_key]['dpi']
        if len(selected_pages) > 0:
            pdf_file.select(selected_pages)
        res = []
        if silent:
            for page in pdf_file:
                pix = page.get_pixmap(dpi=image_dpi)
                data = pix.tobytes(image_format)
                img_page = Image.open(BytesIO(data))
                res.append(img_page)
        else:
            i = 0
            for page in pdf_file:
                output_filename = output_filename_prefix + '_' + str(selected_pages[i] + 1) + '.' + image_format
                pix = page.get_pixmap(dpi=image_dpi)
                self.to_output(task_key, pixmap=pix, output=output_filename)
                data = pix.tobytes(image_format)
                img_page = Image.open(BytesIO(data))
                res.append(img_page)
                i = i + 1
        return res

    def remove(self, input_obj: pymupdf.Document = None, silent: bool = False, **kwargs):
        task_key = 'remove'
        self.set_config_by_task_key(task_key, **kwargs)
        pdf_file = self.trans_object(input_obj, task_key)
        if pdf_file is None:
            return None
        selected_pages = check_pages(pdf_file, self._config[task_key]['pages'])
        if len(selected_pages) > 0:
            pdf_file.delete_pages(selected_pages)
        if silent:
            pass
        else:
            self.to_output(task_key, document=pdf_file)
        return pdf_file

    def extract_images(self, input_obj: pymupdf.Document = None, silent: bool = False, **kwargs):
        task_key = 'extract_images'
        self.set_config_by_task_key(task_key, **kwargs)
        pdf_file = self.trans_object(input_obj, task_key)
        if pdf_file is None:
            return None
        selected_pages = check_pages(pdf_file, self._config[task_key]['pages'])
        if len(selected_pages) > 0:
            pdf_file.select(selected_pages)
        output_filename_prefix = self._config[task_key]['output']
        res = []
        if silent:
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                image_list = page.get_images()
                for image_index, image in enumerate(image_list, start=1):  # enumerate the image list
                    xref = image[0]  # get the XREF of the image
                    pix = pymupdf.Pixmap(pdf_file, xref)  # create a Pixmap
                    if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
                        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                    data = pix.tobytes()
                    img_page = Image.open(BytesIO(data))
                    res.append(img_page)
        else:
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                image_list = page.get_images()
                for image_index, image in enumerate(image_list, start=1):  # enumerate the image list
                    xref = image[0]  # get the XREF of the image
                    pix = pymupdf.Pixmap(pdf_file, xref)  # create a Pixmap
                    if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
                        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                    data = pix.tobytes()
                    img_page = Image.open(BytesIO(data))
                    res.append(img_page)
                    output_filename = output_filename_prefix + '_' + str(page_index) + '_' + str(image_index) + '.png'
                    self.to_output(task_key, pixmap=pix, output=output_filename)
        return res

    def extract_fonts(self, input_obj=None, silent: bool = False, **kwargs):
        task_key = 'extract_fonts'
        self.set_config_by_task_key(task_key, **kwargs)
        pdf_file = self.trans_object(input_obj, task_key)
        if pdf_file is None:
            return None
        output_dir = self.get_output_path(self._config[task_key]['output'])
        if silent:
            output_dir = self.get_log_path(self._config[task_key]['output'])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        fonts = {}
        ret = []
        for page_index in range(pdf_file.page_count):
            fonts_list = pdf_file.get_page_fonts(page_index)
            for font_info in fonts_list:
                if font_info[3] in fonts.keys():
                    pass
                else:
                    fonts[font_info[3]] = font_info[0]
        for font_name, xref in fonts.items():
            name, ext, _, content = pdf_file.extract_font(xref)
            if content is not None:
                font_filename = name + "." + ext
                font_filename = os.path.join(output_dir, font_filename)
                output = open(font_filename, "wb")
                output.write(content)
                output.close()
                ret.append((font_name, font_filename))
        return ret
    #
    # def remove_watermark(self, input_obj=None, silent: bool = False, **kwargs):  # pragma: no cover
    #     task_key = 'remove_watermark'
    #     self.set_config_by_task_key(task_key, **kwargs)
    #     if input_obj is None:
    #         if self.is_default(task_key):
    #             return None
    #         else:
    #             pdf_file = self.trans_object(self._config[task_key]['input'], task_key)
    #     else:
    #         pdf_file = self.trans_object(input_obj, task_key)
    #     pages = len(pdf_file)
    #     watermark = self._config[task_key]['watermark']
    #     for i in range(pages):
    #         page = pdf_file[i]
    #         page.insert_text((20, 20), ' ', fontname='nssc', fontfile=DEFAULT_FONT, render_mode=3)
    #         # for font in page.get_fonts():
    #         #     page.insert_text((20, 20), ' ', fontname=font[4], render_mode=3)
    #         rl = page.search_for(watermark)
    #         for rect in rl:
    #             blocks = page.get_text('dict', clip=rect)["blocks"]
    #             span = blocks[0]['lines'][0]['spans'][0]
    #             font_name = 'nssc'
    #             font_size = span['size']
    #             color = span['color']
    #             origin = fitz.Point(span['origin'])
    #             for font in page.get_fonts():
    #                 if re.search(span['font'] + '$', font[3]):
    #                     font_name = font[4]
    #                     print(font)
    #                     break
    #             block = page.get_text('blocks', clip=rect)[0]
    #             ori_word = block[4] + ''
    #             new_word = ori_word.replace(watermark, '')
    #             # print(ori_word)
    #             # print(new_word)
    #             page.add_redact_annot(rect, text=new_word)
    #             # page.add_redact_annot(block[:4], text=rule['substitute'], fontname=font_name, fontsize=font_size)
    #             # font_name = span['font']
    #             # font_file = self.get_font_file(font_name)
    #             # page.add_redact_annot(rect)
    #             # page.apply_redactions()
    #             # page.insert_text((20, 20), ' ', fontname=font_name, fontfile=font_file, render_mode=3)
    #             # text_length = fitz.get_text_length(rule['substitute'], fontname=font_name, fontsize=font_size)
    #             # font_size = font_size * rect.width / text_length
    #             # print(font_size)
    #             # page.insert_text(origin, rule['substitute'], fontname='nssc', fontsize=font_size, color=color)
    #         page.apply_redactions()
    #     output_filename = self.get_output_path(self._config[task_key]['output'])
    #     if silent:
    #         output_filename = self.get_log_path(self._config[task_key]['output'])
    #     pdf_file.ez_save(output_filename)
    #     pdf_file.close()
    #     return PdfFileReader(open(output_filename, 'rb'))
