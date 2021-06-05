# coding: utf-8

from DataFileElf import DataFileElf
from PIL import Image
import logging
from config import config


class ImageFileElf(DataFileElf):

    def __init__(self):
        super().__init__()

    def init_config(self):
        self._config = config({
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
                    'color': '000',
                    'font': 'arial.ttf',
                    'font_size': 24,
                    'x': 5,
                    'y': 5
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
                            'color': {'type': 'string'},
                            'font': {'type': 'string'},
                            'font_size': {'type': 'number'},
                            'x': {'type': 'number'},
                            'y': {'type': 'number'}
                        }
                    }
                }
            }
        })

    def to_favicon(self, **kwargs):
        self.set_config(**kwargs)
        if self._config.is_default('favicon'):
            logging.warning('"favicon"没有设置正确，请设置后重试。')
        else:
            input_filename = self._config['favicon']['input']
            img = Image.open(self.get_filename_with_path(input_filename))
            if self._config.is_default(['favicon', 'size']):
                icon_sizes = [16, 24, 32, 48, 64, 128, 255]
                for x in icon_sizes:
                    img_resize = img.resize((x, x), Image.ANTIALIAS)
                    output_filename = 'favicon' + str(x) + '.ico'
                    img_resize.save(self.get_output_path(output_filename))
            else:
                favicon_size = self._config['favicon']['size']
                img_resize = img.resize((favicon_size, favicon_size), Image.ANTIALIAS)
                output_filename = 'favicon' + str(favicon_size) + '.ico'
                img_resize.save(self.get_output_path(output_filename))

    def splice(self, **kwargs):
        self.set_config(**kwargs)
        if self._config.is_default('splice'):
            logging.warning('"splice"没有设置正确，请设置后重试。')
        else:
            num_img = len(self._config['splice']['images'])
            output_filename = self._config['splice']['output']
            if num_img > 0:
                width = self._config['splice']['width']
                gap = self._config['splice']['gap']
                width_img = 2 * gap + width
                height_img = gap
                images = []
                locations = []
                y = gap
                locations.append(y)
                for i in range(num_img):
                    filename = self._config['splice']['images'][i]
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
                ret_img.save(self.get_output_path(output_filename))
            else:
                logging.warning('"splice"中没有正确设置"images"参数，请设置后重试。')

    def watermark(self, **kwargs):
        self.set_config(**kwargs)

