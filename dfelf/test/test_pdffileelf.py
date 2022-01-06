import os
import unittest
from dfelf.test.utils import get_platform
from dfelf import PDFFileElf

cwd = os.path.abspath(os.path.dirname(__file__))


class TestPDFFileElf(unittest.TestCase):

    def test_reorganize(self):
        df_elf = PDFFileElf()
        output_filename_01 = 'dive-into-python3-part.pdf'
        output_filename_02 = 'dive-into-python3-part-02.pdf'
        config_01 = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': output_filename_01,
            'pages': [2, 3]
        }
        df_elf.reorganize(**config_01)
        config_02 = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': output_filename_02,
            'pages': [3, 2]
        }
        df_elf.reorganize(**config_02)
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

    def test_image2pdf(self):
        df_elf = PDFFileElf()
        config = {
            'images': [os.path.join(cwd, 'sources', '01.png'), os.path.join(cwd, 'sources', '02.png')],
            'output': 'mr.pdf'
        }
        df_elf.image2pdf(**config)
        if get_platform()=='Windows':
            self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr.pdf')),
                             df_elf.checksum(os.path.join(cwd, 'result', 'mr.pdf')))
        else:
            config_02 = {
                'input': df_elf.get_output_path('mr.pdf'),
                'output': 'mr',
                'format': 'png',
                'pages': [1, 2]
            }
            df_elf.to_image(**config_02)
            self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_1.png')), '2224c910589813a60ede5e281a13d14b')
            self.assertEqual(df_elf.checksum(df_elf.get_output_path('mr_2.png')), 'bcbd7b22565b4e616103b25a5f05c274')

    def test_2image(self):
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


if __name__ == '__main__':
    unittest.main()
