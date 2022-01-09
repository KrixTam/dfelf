import os
import cv2
import base64
import qrcode
from string import Template
from PIL import Image, ImageDraw, ImageFont
from ni.config import Config
from dfelf import DataFileElf
from dfelf.commons import logger


class ImageFileElf(DataFileElf):

    def __init__(self, output_dir=None, output_flag=True):
        super().__init__(output_dir, output_flag)

    def init_config(self):
        self._config = Config({
            'name': 'ImageFileElf',
            'default': {
                'favicon': {
                    'size': -1,
                    'input': 'input_filename'
                },
                'splice': {
                    'output': 'output_filename',
                    'images': [],
                    'width': 700,
                    'gap': 5
                },
                'watermark': {
                    'input': 'input_filename',
                    'output': 'output_filename',
                    'text': 'Krix.Tam',
                    'color': 'FFFFFF',
                    'font': 'arial.ttf',
                    'font_size': 24,
                    'x': 5,
                    'y': 5,
                    'alpha': 50
                },
                '2base64': {
                    'input': 'input_filename',
                    'css_format': False
                },
                'base64': {
                    'input': 'base64 string',
                    'output': 'output_filename'
                },
                'qrcode': {
                    'input': 'string',
                    'output': 'output_filename',
                    'border': 2,
                    'fill_color': "#000000",
                    'back_color': "#FFFFFF"
                },
                'dqrcode': {
                    'input': 'input_filename'
                },
                'resize': {
                    'input': 'input_filename',
                    'output': 'output_filename',
                    'width': 28,
                    'height': 28,
                    'quality': 100,
                    'dpi': 1200
                }
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'favicon': {
                        'type': 'object',
                        'properties': {
                            'size': {'type': 'number'},
                            'input': {'type': 'string'},
                        }
                    },
                    'splice': {
                        'type': 'object',
                        'properties': {
                            'output': {'type': 'string'},
                            'images': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'width': {'type': 'number'},
                            'gap': {'type': 'number'}
                        }
                    },
                    'watermark': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'text': {'type': 'string'},
                            'color': {
                                'type': 'string',
                                'pattern': '[A-Fa-f0-9]{6}'
                            },
                            'font': {'type': 'string'},
                            'font_size': {'type': 'number'},
                            'x': {'type': 'number'},
                            'y': {'type': 'number'},
                            'alpha': {
                                'type': 'number',
                                'minimum': 0,
                                'maximum': 100
                            }
                        }
                    },
                    '2base64': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'css_format': {"type": "boolean"}
                        }
                    },
                    'base64': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'}
                        }
                    },
                    'qrcode': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'border': {
                                'type': 'integer',
                                'minimum': 0
                            },
                            'fill_color': {
                                'type': 'string',
                                'pattern': '^#[A-Fa-f0-9]{6}'
                            },
                            'back_color': {
                                'type': 'string',
                                'pattern': '^#[A-Fa-f0-9]{6}'
                            }
                        }
                    },
                    'dqrcode': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'}
                        }
                    },
                    'resize': {
                        'type': 'object',
                        'properties': {
                            'input': {'type': 'string'},
                            'output': {'type': 'string'},
                            'width': {
                                'type': 'integer',
                                'minimum': 1
                            },
                            'height': {
                                'type': 'integer',
                                'minimum': 1
                            },
                            'quality': {
                                'type': 'integer',
                                'minimum': 1,
                                'maximum': 100
                            },
                            'dpi': {'type': 'integer'}
                        }
                    }
                }
            }
        })

    def to_output(self, task_key, **kwargs):
        if task_key == 'base64':
            output_filename = self.get_output_path(self._config[task_key]['output'])

            if self._output_flag:
                pass
            else:
                output_filename = self.get_log_path(self._config[task_key]['output'])
            with open(output_filename, "wb") as fh:
                fh.write(kwargs['content'])
        else:
            output_filename = self.get_output_path(kwargs['filename'])
            if self._output_flag:
                pass
            else:
                output_filename = self.get_log_path(kwargs['filename'])
            if task_key == 'resize':
                kwargs['img'].save(output_filename, quality=kwargs['quality'], dpi=(kwargs['dpi'], kwargs['dpi']))
            else:
                kwargs['img'].save(output_filename)

    def to_favicon(self, **kwargs):
        task_key = 'favicon'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            img = Image.open(self.get_filename_with_path(input_filename))
            if self._config.is_default([task_key, 'size']):
                icon_sizes = [16, 24, 32, 48, 64, 128, 255]
                res = []
                for x in icon_sizes:
                    img_resize = img.resize((x, x), Image.ANTIALIAS)
                    output_filename = 'favicon' + str(x) + '.ico'
                    self.to_output(task_key, img=img_resize, filename=output_filename)
                    res.append(img_resize)
                return res
            else:
                favicon_size = self._config[task_key]['size']
                img_resize = img.resize((favicon_size, favicon_size), Image.ANTIALIAS)
                output_filename = 'favicon' + str(favicon_size) + '.ico'
                self.to_output(task_key, img=img_resize, filename=output_filename)
                return img_resize

    def splice(self, **kwargs):
        task_key = 'splice'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            num_img = len(self._config[task_key]['images'])
            output_filename = self._config[task_key]['output']
            if num_img > 0:
                width = self._config[task_key]['width']
                gap = self._config[task_key]['gap']
                width_img = 2 * gap + width
                height_img = gap
                images = []
                locations = []
                y = gap
                locations.append(y)
                for i in range(num_img):
                    filename = self._config[task_key]['images'][i]
                    img = Image.open(self.get_filename_with_path(filename))
                    resize_height = int(img.size[1] * width / img.size[0])
                    height_img = height_img + resize_height + gap
                    images.append(img.resize((width, resize_height), Image.ANTIALIAS))
                    y = y + resize_height + gap
                    locations.append(y)
                ret_img = Image.new('RGBA', (width_img, height_img), (255, 255, 255))
                for i in range(num_img):
                    img = images[i]
                    loc = (gap, locations[i])
                    ret_img.paste(img, loc)
                self.to_output(task_key, img=ret_img, filename=output_filename)
                return ret_img
            else:
                logger.warning([3000])
                return None

    def watermark(self, **kwargs):
        task_key = 'watermark'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            img = Image.open(self.get_filename_with_path(input_filename))
            output_filename = self._config[task_key]['output']
            font_draw = ImageFont.truetype(self._config[task_key]['font'], self._config[task_key]['font_size'])
            text = self._config[task_key]['text']
            color = self._config[task_key]['color']
            x = self._config[task_key]['x']
            y = self._config[task_key]['y']
            alpha = int(self._config[task_key]['alpha'] / 100 * 255)
            color = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), alpha)
            loc = (x, y)
            txt_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(txt_img)
            draw.text(loc, text, fill=color, font=font_draw)
            img.paste(txt_img, (0, 0), txt_img)
            self.to_output(task_key, img=img, filename=output_filename)
            return img

    def qrcode(self, **kwargs):
        task_key = 'qrcode'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_string = self._config[task_key]['input']
            output_filename = self._config[task_key]['output']
            border_val = self._config[task_key]['border']
            f_color = self._config[task_key]['fill_color']
            b_color = self._config[task_key]['back_color']
            qr = qrcode.QRCode(border=border_val)
            qr.add_data(input_string)
            qr_image = qr.make_image(fill_color=f_color, back_color=b_color)
            # qr_image.save(self.get_output_path(output_filename))
            self.to_output(task_key, img=qr_image, filename=output_filename)
            return qr_image

    def decode_qrcode(self, **kwargs):
        task_key = 'dqrcode'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            image = cv2.imread(input_filename)
            detector = cv2.QRCodeDetector()
            data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
            if vertices_array is None:
                logger.warning([3001])
                return None
            else:
                logger.info([3002, data])
                return data

    def to_base64(self, **kwargs):
        task_key = '2base64'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None, None
        else:
            input_filename = self._config[task_key]['input']
            file_extension = os.path.splitext(input_filename)[1].replace('.', '')
            with open(input_filename, "rb") as fh:
                encoded = base64.b64encode(fh.read()).decode('ascii')
                if self._config[task_key]['css_format']:
                    encoded = Template('"data:image/${extension};base64,${base64}"').substitute(extension=file_extension, base64=encoded)
                logger.info([3003, encoded])
                return encoded, file_extension

    def from_base64(self, **kwargs):
        task_key = 'base64'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_string = self._config[task_key]['input']
            res = base64.b64decode(input_string)
            self.to_output(task_key, content=res)
            return res

    def resize(self, **kwargs):
        task_key = 'resize'
        self.set_config_by_task_key(task_key, **kwargs)
        if self.is_default(task_key):
            return None
        else:
            input_filename = self._config[task_key]['input']
            output_filename = self._config[task_key]['output']
            width = self._config[task_key]['width']
            height = self._config[task_key]['height']
            quality = self._config[task_key]['quality']
            dpi = self._config[task_key]['dpi']
            img_ori = Image.open(input_filename)
            img_resize = img_ori.resize((width, height), Image.ANTIALIAS)
            # img_resize.save(output_filename, quality=quality, dpi=(dpi, dpi))
            self.to_output(task_key, img=img_resize, filename=output_filename, quality=quality, dpi=dpi)
            return img_resize
