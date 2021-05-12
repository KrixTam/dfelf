# coding: utf-8

import unittest
import os
from PDFFileElf import PDFFileElf


class TestPDFFileElf(unittest.TestCase):

    def test_splitPDF(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join('sources', 'dive-into-python3.pdf')
        output_filename_01 = os.path.join('result', 'dive-into-python3-part.pdf')
        output_filename_02 = os.path.join('result', 'dive-into-python3-part-02.pdf')
        df_elf.splitPDF(input_filename, output_filename_01, [2, 3])
        df_elf.splitPDF(input_filename, output_filename_02, [3, 2])
        # 'fd4c80a337f4599435b2ab31383a4b18' is from the following code:
        # df_elf.checksum(os.path.join('tests', 'sources', 'dive-into-python3-part.pdf'))
        self.assertEqual(df_elf.checksum(output_filename_01), 'fd4c80a337f4599435b2ab31383a4b18')
        self.assertEqual(df_elf.checksum(output_filename_02), '6dedf93bf8afccb5dc2fbd8ea60e6989')


if __name__ == '__main__':
    unittest.main()
