import os
import unittest
from dfelf import PDFFileElf
from PIL import Image, ImageChops
from PyPDF2.pdf import PdfFileReader
from dfelf.commons import is_same_image, to_same_size, read_image
from dfelf.pdffileelf import is_same_pdf
from moment import moment

cwd = os.path.abspath(os.path.dirname(__file__))


class TestPDFFileElf(unittest.TestCase):

    def test_reorganize_01(self):
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
        input_stream.close()
        result_filename_01 = os.path.join(cwd, 'result', 'pdf', output_filename_01)
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_01), result_filename_01))
        result_filename_02 = os.path.join(cwd, 'result', 'pdf', output_filename_02)
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_02), result_filename_02))

    def test_reorganize_02(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
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
        pdf_02 = df_elf.reorganize(input_pdf, True, **config_02)
        input_stream.close()
        result_filename_01 = os.path.join(cwd, 'result', 'pdf', output_filename_01)
        self.assertTrue(is_same_pdf(df_elf.get_log_path(output_filename_01), result_filename_01))
        result_filename_02 = os.path.join(cwd, 'result', 'pdf', output_filename_02)
        self.assertFalse(os.path.exists(df_elf.get_log_path(output_filename_02)))
        self.assertTrue(is_same_pdf(pdf_02, result_filename_02))

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
            'input': df_elf.get_output_path(config['output']),
            'output': 'mr_01',
            'format': 'png',
            'pages': [1, 2]
        }
        df_elf.to_image(**config_02)
        ori_01 = config['images'][0]
        out_01 = df_elf.get_output_path('mr_01_1.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_01.png')
        to_same_size(ori_01, out_01, tmp_filename)
        self.assertTrue(is_same_image(ori_01, tmp_filename, rel_tol=0.05, ignore_alpha=True))
        com_file = os.path.join(cwd, 'result', '01.png')
        self.assertFalse(is_same_image(tmp_filename, com_file, rel_tol=0.05, ignore_alpha=True))
        ori_02 = config['images'][1]
        out_02 = df_elf.get_output_path('mr_01_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, rel_tol=0.05, ignore_alpha=True))

    def test_image2pdf_02(self):
        df_elf = PDFFileElf()
        config = {
            'images': [],
            'output': 'mr.pdf'
        }
        self.assertEqual(None, df_elf.image2pdf(**config))

    def test_image2pdf_03(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        config = {
            'output': 'mr_02.pdf'
        }
        img_01 = os.path.join(cwd, 'sources', '01.png')
        img_02 = os.path.join(cwd, 'sources', '02.png')
        input_imgs = [Image.open(img_01), Image.open(img_02)]
        pdf_file = df_elf.image2pdf(input_imgs, True, **config)
        config_02 = {
            'output': 'mr_02',
            'format': 'png',
            'pages': [1, 2]
        }
        df_elf.to_image(pdf_file, **config_02)
        ori_01 = img_01
        out_01 = df_elf.get_log_path('mr_02_1.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_01.png')
        to_same_size(ori_01, out_01, tmp_filename)
        self.assertTrue(is_same_image(ori_01, tmp_filename, rel_tol=0.05, ignore_alpha=True))
        ori_02 = img_02
        out_02 = df_elf.get_log_path('mr_02_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, rel_tol=0.05, ignore_alpha=True))

    def test_image2pdf_04(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'mr.pdf'
        }
        input_imgs = []
        self.assertEqual(None, df_elf.image2pdf(input_imgs, **config))

    def test_image2pdf_05(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        config = {
            'output': 'mr_05.pdf'
        }
        img_01 = os.path.join(cwd, 'sources', '01.png')
        img_02 = os.path.join(cwd, 'sources', '02.png')
        input_imgs = [Image.open(img_01), Image.open(img_02)]
        pdf_file = df_elf.image2pdf(input_imgs, **config)
        config_02 = {
            'output': 'mr_05',
            'format': 'png',
            'pages': [1, 2]
        }
        df_elf.to_image(pdf_file, **config_02)
        ori_01 = img_01
        out_01 = df_elf.get_log_path('mr_05_1.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_01.png')
        to_same_size(ori_01, out_01, tmp_filename)
        self.assertTrue(is_same_image(ori_01, tmp_filename, rel_tol=0.05, ignore_alpha=True))
        ori_02 = img_02
        out_02 = df_elf.get_log_path('mr_05_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, rel_tol=0.05, ignore_alpha=True))

    def test_2image_01(self):
        df_elf = PDFFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': 'dp_01',
            'format': 'png',
            'pages': [4, 3]
        }
        df_elf.to_image(**config)
        filename_01 = config['output'] + '_4.png'
        filename_02 = config['output'] + '_3.png'
        result_01 = os.path.join(cwd, 'result', 'dp_4.png')
        result_02 = os.path.join(cwd, 'result', 'dp_3.png')
        self.assertTrue(is_same_image(df_elf.get_output_path(filename_01), result_01))
        self.assertTrue(is_same_image(df_elf.get_output_path(filename_02), result_02))

    def test_2image_02(self):
        df_elf = PDFFileElf(output_flag=False)
        config = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': 'dp_02',
            'format': 'png',
            'pages': [4, 3]
        }
        df_elf.to_image(**config)
        filename_01 = config['output'] + '_4.png'
        filename_02 = config['output'] + '_3.png'
        result_01 = os.path.join(cwd, 'result', 'dp_4.png')
        result_02 = os.path.join(cwd, 'result', 'dp_3.png')
        self.assertTrue(is_same_image(df_elf.get_log_path(filename_01), result_01))
        self.assertTrue(is_same_image(df_elf.get_log_path(filename_02), result_02))

    def test_2image_03(self):
        df_elf = PDFFileElf()
        config = {
            'input': os.path.join(cwd, 'sources', 'dive-into-python3.pdf'),
            'output': 'dp_03',
            'format': 'png',
            'pages': [4, 3]
        }
        res = df_elf.to_image(silent=True, **config)
        filename_01 = config['output'] + '_4.png'
        filename_02 = config['output'] + '_3.png'
        result_01 = os.path.join(cwd, 'result', 'dp_4.png')
        result_02 = os.path.join(cwd, 'result', 'dp_3.png')
        self.assertFalse(os.path.exists(df_elf.get_output_path(filename_01)))
        self.assertFalse(os.path.exists(df_elf.get_output_path(filename_02)))
        self.assertTrue(is_same_image(res[0], result_01))
        self.assertTrue(is_same_image(res[1], result_02))

    def test_default(self):
        df_elf = PDFFileElf()
        config = {}
        self.assertEqual(None, df_elf.reorganize(**config))
        self.assertEqual(None, df_elf.image2pdf(**config))
        self.assertEqual(None, df_elf.to_image(**config))

    def test_error_read_image(self):
        with self.assertRaises(TypeError):
            read_image(123)

    def test_is_same_pdf_01(self):
        with self.assertRaises(TypeError):
            is_same_pdf(123, 345)

    def test_is_same_pdf_02(self):
        with self.assertRaises(TypeError):
            is_same_pdf(os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf'), 345)

    def test_is_same_pdf_03(self):
        file_01 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        stream_01 = open(file_01, 'rb')
        pdf_01 = PdfFileReader(stream_01, strict=False)
        file_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02.pdf')
        stream_02 = open(file_02, 'rb')
        pdf_02 = PdfFileReader(stream_02, strict=False)
        self.assertFalse(is_same_pdf(pdf_01, pdf_02))
        stream_01.close()
        stream_02.close()

    def test_is_same_pdf_04(self):
        file_01 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        stream_01 = open(file_01, 'rb')
        pdf_01 = PdfFileReader(stream_01, strict=False)
        file_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02-3.pdf')
        stream_02 = open(file_02, 'rb')
        pdf_02 = PdfFileReader(stream_02, strict=False)
        self.assertFalse(is_same_pdf(pdf_01, pdf_02))
        stream_01.close()
        stream_02.close()


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
