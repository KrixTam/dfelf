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
                'favicon_size': 32
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'input': {'type': 'string'},
                    'output': {'type': 'string'},
                    'favicon_size': {'type': 'number'}
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
