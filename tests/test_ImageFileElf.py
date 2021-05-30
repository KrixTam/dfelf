# coding: utf-8

import unittest
import os
from ImageFileElf import ImageFileElf


class TestImageFileElf(unittest.TestCase):

    def test_to_favicon(self):
        input_filename = os.path.join('sources', 'icon.png')
        df_elf = ImageFileElf()
        df_elf.to_favicon(input=input_filename)
        icon_sizes = [16, 24, 32, 48, 64, 128, 255]
        for x in icon_sizes:
            filename = 'favicon' + str(x) + '.ico'
            result_filename = os.path.join('result', 'IFE', filename)
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)), df_elf.checksum(df_elf.get_filename_with_path(result_filename)))
        df_elf.to_favicon(input=input_filename, favicon_size=192)
        filename = 'favicon192.ico'
        result_filename = os.path.join('result', 'IFE', filename)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename)),
                         df_elf.checksum(df_elf.get_filename_with_path(result_filename)))


if __name__ == '__main__':
    unittest.main()
