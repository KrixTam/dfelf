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
                'input': 'input_filename',
                'output': 'output_filename',
                'favicon_size': 32,
                'splice': {
                    'images': [],
                    'width': 700,
                    'gap': 5
                }
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'input': {'type': 'string'},
                    'output': {'type': 'string'},
                    'favicon_size': {'type': 'number'},
                    'splice': {
                        'type': 'object',
                        'properties': {
                            'images': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                            'width': {'type': 'number'},
                            'gap': {'type': 'number'}
                        }
                    }
                }
            }
        })

    def to_favicon(self, **kwargs):
        self.set_config(**kwargs)
        input_filename = self._config['input']
        img = Image.open(self.get_filename_with_path(input_filename))
        if self._config.is_default('favicon_size'):
            icon_sizes = [16, 24, 32, 48, 64, 128, 255]
            for x in icon_sizes:
                img_resize = img.resize((x, x), Image.ANTIALIAS)
                output_filename = 'favicon' + str(x) + '.ico'
                img_resize.save(self.get_output_path(output_filename))
        else:
            favicon_size = self._config['favicon_size']
            img_resize = img.resize((favicon_size, favicon_size), Image.ANTIALIAS)
            output_filename = 'favicon' + str(favicon_size) + '.ico'
            img_resize.save(self.get_output_path(output_filename))

    def splice(self, **kwargs):
        self.set_config(**kwargs)
        if self._config.is_default('splice'):
            num_img = len(self._config['splice']['images'])
            output_filename = self._config['output']
            if num_img > 0:
                width = self._config['splice']['width']
                gap = self._config['splice']['gap']
                width_img = 2 * gap + width
                height_img = 2 * gap
                images = []
                locations = []
                y = gap
                for i in range(num_img):
                    filename = self._config['splice']['images'][i]
                    img = Image.open(self.get_filename_with_path(filename))
                    resize_height = img.size[1] * width / img.size[0]
                    height_img = height_img + resize_height
                    images.append(img.resize((width, resize_height), Image.ANTIALIAS))
                    if i == 0:
                        pass
                    else:
                        y = y + resize_height
                    locations.append(y)
                ret_img = Image.new('RGBA', (width_img, height_img), (255, 255, 255))
                for i in range(num_img):
                    img = images[i]
                    loc = (gap, locations[i])
                    ret_img.paste(img, loc)
                ret_img.save(self.get_output_path(output_filename))
            else:
                logging.warning('"splice"中没有正确设置"images"参数，请设置后重试。')
        else:
            logging.warning('"splice"没有设置正确，请设置后重试。')

    def watermark(self, **kwargs):
        self.set_config(**kwargs)

