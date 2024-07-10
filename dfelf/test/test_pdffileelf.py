import os
import unittest
from dfelf import PDFFileElf
from PIL import Image
import pymupdf
from dfelf.commons import is_same_image, to_same_size, read_image, contain_chinese
from dfelf.pdffileelf import is_same_pdf, open_pdf
from moment import moment
from dfelf.test.utils import get_files

cwd = os.path.abspath(os.path.dirname(__file__))


class TestPDFFileElf(unittest.TestCase):

    def test_default(self):
        df_elf = PDFFileElf()
        config = {}
        self.assertEqual(None, df_elf.create(**config))
        self.assertEqual(None, df_elf.to_image(**config))
        self.assertEqual(None, df_elf.remove(**config))
        self.assertEqual(None, df_elf.image2pdf(**config))
        self.assertEqual(None, df_elf.extract_images(**config))
        self.assertEqual(None, df_elf.extract_fonts(**config))
        # self.assertEqual(None, df_elf.remove_watermark(**config))

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
        self.assertTrue(is_same_image(df_elf.get_output_path(filename_02), result_02, ssim_only=True))

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
        self.assertTrue(is_same_image(df_elf.get_log_path(filename_02), result_02, ssim_only=True))

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
        self.assertTrue(is_same_image(res[1], result_02, ssim_only=True))

    def test_create_reorganize_01(self):
        df_elf = PDFFileElf()
        output_filename_01 = 'dive-into-python3-part.pdf'
        output_filename_02 = 'dive-into-python3-part-02.pdf'
        input_filename = os.path.join(cwd, 'sources', 'dive-into-python3.pdf')
        config_01 = {
            'input': [
                {
                    'file': input_filename,
                    'pages': [2, 3, 499]
                }],
            'output': output_filename_01,
        }
        df_elf.create(**config_01)
        result_filename_01 = os.path.join(cwd, 'result', 'pdf', output_filename_01)
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_01), result_filename_01))
        config_02 = {
            'output': output_filename_02
        }
        input_pdf = pymupdf.open(input_filename)
        input_obj = [{'file': input_pdf, 'pages': [3, 2]}]
        df_elf.create(input_obj, **config_02)
        input_pdf.close()
        result_filename_02 = os.path.join(cwd, 'result', 'pdf', output_filename_02)
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_02), result_filename_02))

    def test_create_reorganize_02(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        output_filename_01 = 'dive-into-python3-part.pdf'
        output_filename_02 = 'dive-into-python3-part-02.pdf'
        input_filename = os.path.join(cwd, 'sources', 'dive-into-python3.pdf')
        config_01 = {
            'input': [{'file': input_filename, 'pages': [2, 3, 499]}],
            'output': output_filename_01
        }
        df_elf.create(**config_01)
        config_02 = {
            'output': output_filename_02,
            'pages': [3, 2]
        }
        input_pdf = pymupdf.open(input_filename)
        input_obj = [{'file': input_pdf, 'pages': [3, 2]}]
        pdf_02 = df_elf.create(input_obj, True, **config_02)
        result_filename_01 = os.path.join(cwd, 'result', 'pdf', output_filename_01)
        self.assertTrue(is_same_pdf(df_elf.get_log_path(output_filename_01), result_filename_01))
        result_filename_02 = os.path.join(cwd, 'result', 'pdf', output_filename_02)
        self.assertFalse(os.path.exists(df_elf.get_log_path(output_filename_02)))
        self.assertTrue(is_same_pdf(pdf_02, result_filename_02))

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
        pdf_01 = open_pdf(file_01)
        file_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02.pdf')
        pdf_02 = open_pdf(file_02)
        self.assertFalse(is_same_pdf(pdf_01, pdf_02))
        pdf_01.close()
        pdf_02.close()

    def test_is_same_pdf_04(self):
        file_01 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        pdf_01 = open_pdf(file_01)
        file_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02-3.pdf')
        pdf_02 = open_pdf(file_02)
        self.assertFalse(is_same_pdf(pdf_01, pdf_02))
        pdf_01.close()
        pdf_02.close()

    def test_create_merge_01(self):
        df_elf = PDFFileElf()
        input_01 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        input_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02.pdf')
        output_filename = 'dive-into-python3-part.merge.pdf'
        config = {
            'input': [
                {'file': input_01, 'pages': []},
                {'file': input_02, 'pages': []}
            ],
            'output': output_filename
        }
        df_elf.create(**config)
        result_filename = os.path.join(cwd, 'result', 'pdf', output_filename)
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename), result_filename))

    def test_create_merge_02(self):
        df_elf = PDFFileElf()
        input_01 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        input_02 = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part-02.pdf')
        output_filename = 'dive-into-python3-part.merge.pdf'
        input_files = []
        pdf_file = open_pdf(input_01)
        input_files.append({'file': pdf_file, 'pages': []})
        pdf_file = open_pdf(input_02)
        input_files.append({'file': pdf_file, 'pages': []})
        config = {
            'output': output_filename
        }
        res = df_elf.create(input_files, True, **config)
        result_filename = os.path.join(cwd, 'result', 'pdf', output_filename)
        self.assertTrue(is_same_pdf(res, result_filename))

    def test_remove_01(self):
        df_elf = PDFFileElf()
        output_filename_01 = 'dive-into-python3-part_remove_01_01.pdf'
        output_filename_02 = 'dive-into-python3-part_remove_01_02.pdf'
        input_filename = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.merge.pdf')
        config_01 = {
            'input': input_filename,
            'output': output_filename_01,
            'pages': [3, 4, 499]
        }
        df_elf.remove(**config_01)
        config_02 = {
            'output': output_filename_02,
            'pages': [4, 3]
        }
        pdf_file = open_pdf(input_filename)
        df_elf.remove(pdf_file, **config_02)
        pdf_file.close()
        result_filename = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_01), result_filename))
        self.assertTrue(is_same_pdf(df_elf.get_output_path(output_filename_02), result_filename))

    def test_remove_02(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        output_filename_01 = 'dive-into-python3-part_remove_02_01.pdf'
        output_filename_02 = 'dive-into-python3-part_remove_02_02.pdf'
        input_filename = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.merge.pdf')
        config_01 = {
            'input': input_filename,
            'output': output_filename_01,
            'pages': [3, 4, 499]
        }
        df_elf.remove(**config_01)
        config_02 = {
            'output': output_filename_02,
            'pages': [4, 3]
        }
        pdf_file = open_pdf(input_filename)
        pdf_02 = df_elf.remove(pdf_file, True, **config_02)
        pdf_file.close()
        result_filename = os.path.join(cwd, 'result', 'pdf', 'dive-into-python3-part.pdf')
        self.assertTrue(is_same_pdf(df_elf.get_log_path(output_filename_01), result_filename))
        self.assertFalse(os.path.exists(df_elf.get_log_path(output_filename_02)))
        self.assertTrue(is_same_pdf(pdf_02, result_filename))

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
        self.assertTrue(is_same_image(ori_01, tmp_filename, ssim_only=True))
        com_file = os.path.join(cwd, 'result', '01.png')
        self.assertFalse(is_same_image(tmp_filename, com_file, ssim_only=True))
        ori_02 = config['images'][1]
        out_02 = df_elf.get_output_path('mr_01_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, ssim_only=True))

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
        self.assertTrue(is_same_image(ori_01, tmp_filename, ssim_only=True))
        ori_02 = img_02
        out_02 = df_elf.get_log_path('mr_02_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, ssim_only=True))

    def test_image2pdf_04(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'mr.pdf'
        }
        input_images = []
        self.assertEqual(None, df_elf.image2pdf(input_images, **config))

    def test_image2pdf_05(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        config = {
            'output': 'mr_05.pdf'
        }
        img_01 = os.path.join(cwd, 'sources', '01.png')
        img_02 = os.path.join(cwd, 'sources', '02.png')
        input_images = [Image.open(img_01), Image.open(img_02)]
        pdf_file = df_elf.image2pdf(input_images, **config)
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
        self.assertTrue(is_same_image(ori_01, tmp_filename, ssim_only=True))
        ori_02 = img_02
        out_02 = df_elf.get_log_path('mr_05_2.png')
        tmp_filename = df_elf.get_log_path('tmp_' + str(moment().unix_timestamp()) + '_02.png')
        to_same_size(ori_02, out_02, tmp_filename)
        self.assertTrue(is_same_image(ori_02, tmp_filename, ssim_only=True))

    def test_extract_images_01(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.jp2.pdf')
        config = {
            'input': input_filename,
            'output': 'extract_images_01',
            'pages': []
        }
        images = df_elf.extract_images(**config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.jp2')
        self.assertTrue(is_same_image(df_elf.get_output_path(config['output'] + '_0_1.png'),
                                      result_filename))

    def test_extract_images_02(self):
        df_elf = PDFFileElf()
        df_elf.shutdown_output()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.jpg.pdf')
        config = {
            'input': input_filename,
            'output': 'extract_images_02'
        }
        images = df_elf.extract_images(**config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.jpg')
        self.assertTrue(is_same_image(df_elf.get_log_path(config['output'] + '_0_1.png'),
                                      result_filename))

    def test_extract_images_03(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.png.pdf')
        config = {
            'output': 'extract_images_03',
            'pages': []
        }
        pdf_file = open_pdf(input_filename)
        images = df_elf.extract_images(pdf_file, **config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.png')
        self.assertTrue(is_same_image(df_elf.get_output_path(config['output'] + '_2_1.png'),
                                      result_filename, ssim_only=True))

    def test_extract_images_04(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.tif.pdf')
        config = {
            'input': input_filename,
            'output': 'extract_images_04',
            'pages': []
        }
        images = df_elf.extract_images(**config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.tif')
        self.assertTrue(is_same_image(df_elf.get_output_path(config['output'] + '_0_1.png'),
                                      result_filename))

    def test_extract_images_05(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.tiff.pdf')
        config = {
            'input': input_filename,
            'output': 'extract_images_05',
            'pages': []
        }
        images = df_elf.extract_images(**config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.tiff')
        self.assertTrue(is_same_image(df_elf.get_output_path(config['output'] + '_0_1.png'),
                                      result_filename, ssim_only=True))

    def test_extract_images_06(self):
        df_elf = PDFFileElf()
        input_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.png.02.pdf')
        config = {
            'output': 'extract_images_06',
            'pages': []
        }
        pdf_file = open_pdf(input_filename)
        images = df_elf.extract_images(pdf_file, True, **config)
        result_filename = os.path.join(cwd, 'result', 'pdf', 'extract_images', 'test.02.png')
        self.assertTrue(is_same_image(images[0], result_filename, ssim_only=True))

    def test_contain_chinese_01(self):
        self.assertTrue(contain_chinese('123你好abc'))

    def test_contain_chinese_02(self):
        self.assertFalse(contain_chinese('123abc'))

    def test_extract_fonts_01(self):
        df_elf = PDFFileElf()
        output_dir = 'extract_fonts_01'
        ori_filename = 'dive-into-python3-part.pdf'
        config = {
            'input': os.path.join(cwd, 'result', 'pdf', ori_filename),
            'output': output_dir
        }
        result = ['PXAAAA+Georgia,Bold.ttf',
                  'PXAAAB+FreeSerif.ttf',
                  'PXAAAC+GillSansMT,Italic.ttf',
                  'PXAAAD+GillSansMT.ttf',
                  'PXAAAF+TimesNewRoman.ttf',
                  'PXAAAG+AndaleMono.ttf']
        ret = df_elf.extract_fonts(**config)
        self.assertEqual(len(ret), 6)
        font_files = get_files(df_elf.get_output_path(config['output']))
        if ori_filename in font_files:
            font_files.remove(ori_filename)  # pragma: no cover
        self.assertEqual(len(font_files), len(result))
        all_true = True
        for f in font_files:
            if f in result:
                pass
            else:
                all_true = False  # pragma: no cover
                break  # pragma: no cover
        self.assertTrue(all_true)

    def test_extract_fonts_02(self):
        df_elf = PDFFileElf()
        output_dir = 'extract_fonts_02'
        ori_filename = 'dive-into-python3-part.pdf'
        input_filename = os.path.join(cwd, 'result', 'pdf', ori_filename)
        config = {
            'input': input_filename,
            'output': output_dir
        }
        result = ['PXAAAA+Georgia,Bold.ttf',
                  'PXAAAB+FreeSerif.ttf',
                  'PXAAAC+GillSansMT,Italic.ttf',
                  'PXAAAD+GillSansMT.ttf',
                  'PXAAAF+TimesNewRoman.ttf',
                  'PXAAAG+AndaleMono.ttf']
        pdf_file = open_pdf(input_filename)
        ret = df_elf.extract_fonts(pdf_file, True, **config)
        self.assertEqual(len(ret), 6)
        font_files = get_files(df_elf.get_log_path(config['output']))
        if ori_filename in font_files:
            font_files.remove(ori_filename)  # pragma: no cover
        self.assertEqual(len(font_files), len(result))
        all_true = True
        for f in font_files:
            if f in result:
                pass
            else:
                all_true = False  # pragma: no cover
                break  # pragma: no cover
        self.assertTrue(all_true)
    '''
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

    
    def test_trans_object_error_01(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'mr_02.pdf'
        }
        img_01 = os.path.join(cwd, 'sources', '01.png')
        img_02 = os.path.join(cwd, 'sources', '02.png')
        input_imgs = [123, Image.open(img_02)]
        with self.assertRaises(TypeError):
            df_elf.image2pdf(input_imgs, True, **config)

    def test_trans_object_error_02(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'test_02.pdf'
        }
        with self.assertRaises(TypeError):
            df_elf.extract_fonts(123, True, **config)

    def test_trans_object_error_03(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'extract_images_06_',
            'pages': []
        }
        with self.assertRaises(TypeError):
            df_elf.extract_images(123, True, **config)

    def test_trans_object_error_04(self):
        df_elf = PDFFileElf()
        config = {
            'output': 'test_02.pdf'
        }
        with self.assertRaises(TypeError):
            df_elf.remove_watermark(123, True, **config)
    '''

if __name__ == '__main__':
    unittest.main()  # pragma: no cover
