from ni.config.tools import Logger
import math
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray, rgba2rgb
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import os
import re
from random import randint
from moment import moment

try:
    import importlib.resources as pkg_resources
except ImportError:  # pragma: no cover
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # pragma: no cover
from dfelf.res import Noto_Sans_SC
DEFAULT_FONT = os.path.join(pkg_resources.files(Noto_Sans_SC), 'NotoSansSC-Regular.otf')

# 0-999: Commons
# 1000-1999: DataFileElf
# 2000-2999: CSVFileElf
# 3000-3999: ImageFileElf
# 4000-4999: PDFFileElf


ERROR_DEF = {
    '0': '[{0}] 图像相似度不符合要求（{3}, {4}），MSE为{1}，SSIM为{2}。',
    '1': '[{0}] read_image中的参数"image_file"类型错误，应为Image.Image或者str。',
    '1000': '[{0}] "{1}"没有设置正确（不能直接使用默认设置值），请设置后重试。',
    '2000': '[{0}] 存在需要进行去重处理的值，详细请查阅文件：{1}\n{2}',
    '2001': '[{0}] 如下重复值将被去除，详细请查阅文件：{1}\n{2}',
    '2002': '[{0}] "split"中的"key"不存在，请检查数据文件"{1}"是否存在该字段"{2}"。',
    '2003': '[{0}] "drop_duplicates"中的"subset"参数({1})类型({2})错误，应为str或list。',
    '2004': '[{0}] "{1}"的输入对象参数"input_obj"类型({2})错误，应为{3}。',
    '2005': '[{0}] "{1}"的输入对象参数"input_obj"列表中的对象类型({2})错误，列表中每个对象类型为{3}或{4}。',
    '2006': '[{0}] "{1}"的输入对象参数"input_obj"类型({2})错误，应为{3}或{4}。',
    '3000': '[{0}] "splice"中没有正确设置"input"参数，请设置后重试。',
    '3001': '[{0}] 图片中未能解析到二维码。',
    '3002': '[{0}] 解码成功，内容为：\n{1}',
    '3003': '[{0}] 文件"{1}"转换为base64成功。',
    '3004': '[{0}] 坐标数据{1}异常，无法进行裁剪处理。',
    '3005': '[{0}] 坐标数据{1}异常，无法进行马赛克处理。',
    '3006': '[{0}] most_used_color方法中的参数"img"类型错误，应为Image.Image或者numpy.ndarray。',
    '3007': '[{0}] ImageFileElf.decode_qrcode中的参数"input_obj"类型{1}错误，应为Image.Image或者numpy.ndarray。',
    '3008': '[{0}] "{1}"的输入对象参数"input_obj"类型({2})错误，应为{3}或{4}。',
    '3009': '[{0}] ImageFileElf.decode_qrcode中的参数"input_obj"指向的文件"{1}"不存在。',
    '4000': '[{0}] PDF文件"{1}"中不存在第{2}的内容，请检查PDF原文档的内容正确性或者配置正确性。',
    '4001': '[{0}] "from_images"没有设置，请设置后重试。',
    '4002': '[{0}] "{1}"的输入对象参数"input_obj"类型({2})错误，应为{3}或{4}。',
    '4003': '[{0}] 文档<"{1}">一共有{2}页，不存在第{3}页。',
    '4004': '[{0}] 文档<"{1}">的页码参数"pages"设置错误，请检查后重新运行程序。',
    '4005': '[{0}] open_pdf的参数类型({1})错误，应为pymupdf.Document或str。'
}

logger = Logger(ERROR_DEF, 'dfelf')


def is_same_image(file_1, file_2, rel_tol_mse=0.015, rel_tol_ssim=0.05, ssim_only=False):
    m, s = mse_n_ssim(file_1, file_2)
    if ssim_only:
        flag = math.isclose(s, 1.0, rel_tol=rel_tol_ssim)
    else:
        flag = math.isclose(1.0 - m, 1.0, rel_tol=rel_tol_mse) and math.isclose(s, 1.0, rel_tol=rel_tol_ssim)
    if flag:
        return True
    else:
        logger.warning([0, m, s, rel_tol_mse, rel_tol_ssim])
        return False


def read_image(image_file):
    if isinstance(image_file, str):
        image = imread(image_file, plugin='pil')
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = rgba2rgb(image)
        if image.dtype == np.uint8:
            pass
        else:
            image = np.uint8(image * 255)
        return image
    if isinstance(image_file, Image.Image):
        open_cv_image = np.asarray(image_file.convert('RGB'))
        # 将RGB转换为BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image
    if isinstance(image_file, np.ndarray):
        return image_file.copy()
    logger.warning([1])
    raise TypeError


def mse_n_ssim(file_1, file_2):
    img_1 = read_image(file_1)
    img_2 = read_image(file_2)
    mse = np.linalg.norm(img_1.astype(np.float64) - img_2.astype(np.float64)) / (img_1.shape[0] * img_1.shape[1])
    if len(img_1.shape) == 3:
        img_1_gray = rgb2gray(img_1)
    else:
        img_1_gray = img_1
    if len(img_2.shape) == 3:
        img_2_gray = rgb2gray(img_2)
    else:
        img_2_gray = img_2
    (score, diff) = ssim(img_1_gray, img_2_gray, data_range=1.0, full=True)
    return mse, score


def to_same_size(file_ori, file_todo, file_output):
    img_ori = Image.open(file_ori)
    img_todo = Image.open(file_todo)
    width_ori, height_ori = img_ori.size
    width_todo, height_todo = img_todo.size
    width = width_ori
    height = round(height_todo * 1.0 / width_todo * width_ori)
    img_resize = img_todo.resize((width, height), Image.Resampling.LANCZOS)
    img_resize.save(file_output)
    img_ori.close()
    img_todo.close()
    img_resize.close()


chinese_checker = re.compile(u'[\u4e00-\u9fa5]')


def contain_chinese(input_string: str):
    return chinese_checker.search(input_string)


def random_name():
    return str(moment().unix()) + str(randint(0, 9))
