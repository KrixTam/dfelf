import os
import unittest
from dfelf.test.utils import get_platform
from dfelf import PDFFileElf
from PIL import Image
from PyPDF2.pdf import PdfFileReader

cwd = os.path.abspath(os.path.dirname(__file__))


class TestPDFFileElf(unittest.TestCase):

    def test_reorganize(self):
        df_elf = PDFFileElf()
        output_filename_01 = 'dive-into-python3-part.pdf'
        output_filename_02 = 'dive-into-python3-part-02.pdf'
        input_filename = os.path.join(cwd, 'sources', 'dive-into-python3.pdf')
        config_01 = {
            'input': input_filename,
            'output': output_filename_01,
            'pages': [2, 3, 499]
        }
        df_elf.reorganize(**config_01)
        config_02 = {
            'output': output_filename_02,
            'pages': [3, 2]
        }
        input_stream = open(input_filename, 'rb')
        input_pdf = PdfFileReader(input_stream)
        df_elf.reorganize(input_pdf, **config_02)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(output_filename_01)), 'fd4c80a337f4599435b2ab31383a4b18')
        self.assertEqual(df_elf.checksum(df_elf.get_output_path(output_filename_02)), '6dedf93bf8afccb5dc2fbd8ea60e6989')

    def test_generate_config_file(self):
        df_elf = PDFFileElf()
        default_cfg_file = os.path.join(cwd, 'sources', 'PDFFileElf_default.cfg')
        output_filename_01 = os.path.join('output', 'PDFFileElf_default.cfg')
        output_filename_02 = os.path.join('output', 'PDFFileElf.cfg')
        df_elf.generate_config_file(output_filename_01)
        config = {'input': 'abc.pdf', 'output': 'cde.pdf', 'pages': [1, 3, 2]}
        df_elf.generate_config_file(output_filename_02, reorganize=config)
        self.assertEqual(df_elf.checksum(output_filename_01), df_elf.checksum(default_cfg_file))
        c = df_elf.get_config()
        self.assertEqual(c['reorganize']['input'], 'abc.pdf')
        self.assertEqual(c['reorganize']['output'], 'cde.pdf')
        self.assertEqual(c['reorganize']['pages'], [1, 3, 2])

    def test_image2pdf_01(self):
        df_elf = PDFFileElf()
        config = {
            'images': [os.path.join(cwd, 'sources', '01.png'), os.path.join(cwd, 'sources', '02.png')],
            'output': 'mr_01.pdf'
        }
        df_elf.image2pdf(**config)
        config_02 = {
            'input': df_elf.get_output_path('mr_01.pdf'),
            'output': 'mr_01',
            'format': 'png',
            'pages': [1, 2]
        }
        df_elf.to_image(**config_02)
        res_01 = df_elf.checksum(os.path.join(cwd, 'result', 'mr_01_1.png'))
        res_02 = df_elf.checksum(os.path.join(cwd, 'result', 'mr_01_2.png'))
        self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_01_1.png')), res_01)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_01_2.png')), res_02)

    def test_image2pdf_02(self):
        df_elf = PDFFileElf()
        config = {
            'images': [],
            'output': 'mr.pdf'
        }
        self.assertEqual(None, df_elf.image2pdf(**config))

    def test_image2pdf_03(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'mr_02.pdf'
        }
        input_imgs = [Image.open(os.path.join(cwd, 'sources', '01.png')), Image.open(os.path.join(cwd, 'sources', '02.png'))]
        df_elf.image2pdf(input_imgs, **config)
        input_filename = df_elf.get_output_path('mr_02.pdf')
        config_02 = {
            'output': 'mr_02',
            'format': 'png',
            'pages': [1, 2]
        }
        input_stream = open(input_filename, 'rb')
        pdf_file = PdfFileReader(input_stream, strict=False)
        df_elf.to_image(pdf_file, **config_02)
        res_01 = df_elf.checksum(os.path.join(cwd, 'result', 'mr_01_1.png'))
        res_02 = df_elf.checksum(os.path.join(cwd, 'result', 'mr_01_2.png'))
        self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_01_1.png')), res_01)
        self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_01_2.png')), res_02)

    def test_image2pdf_04(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'mr.pdf'
        }
        input_imgs = []
        self.assertEqual(None, df_elf.image2pdf(input_imgs, **config))

    def test_2image_01(self):
        df_elf = PDFFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': 'dp',
            'format': 'png',
            'pages': [4, 3]
        }
        df_elf.to_image(**config)
        filename_01 = config['output'] + '_4.png'
        filename_02 = config['output'] + '_3.png'
        if get_platform() == 'Windows':
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename_01)),
                             df_elf.checksum(os.path.join(cwd, 'result', filename_01)))
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename_02)),
                             df_elf.checksum(os.path.join(cwd, 'result', filename_02)))
        else:
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename_01)), '83da825a636756f03213276f393fcab7')
            self.assertEqual(df_elf.checksum(df_elf.get_output_path(filename_02)), '00cf3701dafd2d753d865dc0779fb764')

    def test_2image_02(self):
        df_elf = PDFFileElf(output_flag=False)
        config = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': 'dp',
            'format': 'png',
            'pages': [4, 3]
        }
        df_elf.to_image(**config)
        filename_01 = config['output'] + '_4.png'
        filename_02 = config['output'] + '_3.png'
        if get_platform() == 'Windows':
            self.assertEqual(df_elf.checksum(df_elf.get_log_path(filename_01)),
                             df_elf.checksum(os.path.join(cwd, 'result', filename_01)))
            self.assertEqual(df_elf.checksum(df_elf.get_log_path(filename_02)),
                             df_elf.checksum(os.path.join(cwd, 'result', filename_02)))
        else:
            self.assertEqual(df_elf.checksum(df_elf.get_log_path(filename_01)), '83da825a636756f03213276f393fcab7')
            self.assertEqual(df_elf.checksum(df_elf.get_log_path(filename_02)), '00cf3701dafd2d753d865dc0779fb764')

    def test_default(self):
        df_elf = PDFFileElf()
        config = {}
        self.assertEqual(None, df_elf.reorganize(**config))
        self.assertEqual(None, df_elf.image2pdf(**config))
        self.assertEqual(None, df_elf.to_image(**config))


if __name__ == '__main__':
    unittest.main()
