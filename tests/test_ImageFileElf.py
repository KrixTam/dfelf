# coding: utf-8

import unittest
import os
from ImageFileElf import ImageFileElf


class TestImageFileElf(unittest.TestCase):

    def test_to_favicon(self):
        input_filename = os.path.join('sources', 'icon.png')
        favicon_settings = {'input': input_filename}
        df_elf = ImageFileElf()
        df_elf.to_favicon(**favicon_settings)
        icon_sizes = [16, 24, 32, 48, 64, 128, 255]
        for x in icon_sizes:
            filename = 'favicon' + str(x) + '.ico'
            result_filename = os.path.join('result', 'IFE', filename)
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)), df_elf.checksum(df_elf.get_filename_with_path(result_filename)))
        favicon_settings = {
            'input': input_filename,
            'size': 192
        }
        df_elf.to_favicon(**favicon_settings)
        filename = 'favicon192.ico'
        result_filename = os.path.join('result', 'IFE', filename)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)),
                         df_elf.checksum(df_elf.get_filename_with_path(result_filename)))

    def test_splice(self):
        input_filename = os.path.join('sources', 'icon.png')
        filename = 'icon_splice.png'
        df_elf = ImageFileElf()
        splice_config = {
            'output': filename,
            'images': [input_filename, input_filename],
            'width': 125
        }
        df_elf.splice(**splice_config)
        result_filename = os.path.join('result', filename)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)),
                         df_elf.checksum(df_elf.get_filename_with_path(result_filename)))

    def test_watermark(self):
        df_elf = ImageFileElf()
        ttf = os.path.join('sources', 'arial.ttf')
        input_filename = os.path.join('sources', 'icon.png')
        filename = 'icon_watermark.png'
        watermark = {
            'input': input_filename,
            'output': filename,
            'text': 'Krix.Tam',
            'color': 'FFFFFF',
            'font': ttf,
            'font_size': 14,
            'alpha': 20
        }
        df_elf.watermark(**watermark)
        result_filename = os.path.join('result', filename)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)),
                         df_elf.checksum(df_elf.get_filename_with_path(result_filename)))


if __name__ == '__main__':
    unittest.main()
