# coding: utf-8

import unittest
import os
from PDFFileElf import PDFFileElf


class TestPDFFileElf(unittest.TestCase):

    def test_reorganize_pdf(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join('sources', 'dive-into-python3.pdf')
        output_filename_01 = os.path.join('result', 'dive-into-python3-part.pdf')
        output_filename_02 = os.path.join('result', 'dive-into-python3-part-02.pdf')
        df_elf.reorganize_pdf(input_filename, output_filename_01, [2, 3])
        df_elf.reorganize_pdf(input_filename, output_filename_02, [3, 2])
        # 'fd4c80a337f4599435b2ab31383a4b18' is from the following code:
        # df_elf.checksum(os.path.join('tests', 'sources', 'dive-into-python3-part.pdf'))
        self.assertEqual(df_elf.checksum(output_filename_01), 'fd4c80a337f4599435b2ab31383a4b18')
        self.assertEqual(df_elf.checksum(output_filename_02), '6dedf93bf8afccb5dc2fbd8ea60e6989')

    def test_generate_config_file(self):
        df_elf = PDFFileElf()
        default_cfg_file = os.path.join('sources', 'PDFFileElf_default.cfg')
        output_filename_01 = os.path.join('result', 'PDFFileElf_default.cfg')
        output_filename_02 = os.path.join('result', 'PDFFileElf.cfg')
        df_elf.generate_config_file(output_filename_01)
        df_elf.generate_config_file(output_filename_02, 'abc.pdf', 'cde.pdf', [1, 3, 2])
        self.assertEqual(df_elf.checksum(output_filename_01), df_elf.checksum(default_cfg_file))
        self.assertEqual(df_elf['input'], 'abc.pdf')
        self.assertEqual(df_elf['output'], 'cde.pdf')
        self.assertEqual(df_elf['concat'], [1, 3, 2])


if __name__ == '__main__':
    unittest.main()
