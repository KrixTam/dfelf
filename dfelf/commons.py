from ni.config.tools import Logger
import math
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image

# 0-999: Commons
# 1000-1999: DataFileElf
# 2000-2999: CSVFileElf
# 3000-3999: ImageFileElf
# 4000-4999: PDFFileElf


ERROR_DEF = {
    '0': '[{0}] 图像相似度不符合要求（{3}），MSE为{1}，SSIM为{2}。',
    '1000': '[{0}] "{1}"没有设置正确（不能直接使用默认设置值），请设置后重试。',
    '2000': '[{0}] 存在需要进行去重处理的值，详细请查阅文件：{1}\n{2}',
    '2001': '[{0}] 如下重复值将被去除，详细请查阅文件：{1}\n{2}',
    '2002': '[{0}] "split"中的"key"不存在，请检查数据文件"{1}"是否存在该字段"{2}"。',
    '3000': '[{0}] "splice"中没有正确设置"images"参数，请设置后重试。',
    '3001': '[{0}] 图片中未能解析到二维码。',
    '3002': '[{0}] 解码成功：\n{1}',
    '3003': '[{0}] 转换为base64成功：\n{1}',
    '4000': '[{0}] PDF文件"{1}"中不存在第{2}的内容，请检查PDF原文档的内容正确性或者配置正确性。',
    '4001': '[{0}] "from_images"没有设置，请设置后重试。'
}

logger = Logger(ERROR_DEF, 'dfelf')


def is_same_image(file_1, file_2, rel_tol=0.0001, ignore_alpha=False):
    m, s = mse_n_ssim(file_1, file_2)
    if ignore_alpha:
        flag = math.isclose(s, 1.0, rel_tol=rel_tol)
    else:
        flag = math.isclose(1.0 - m, 1.0, rel_tol=rel_tol) and math.isclose(s, 1.0, rel_tol=rel_tol)
    if flag:
        return True
    else:
        logger.warning([0, m, s, rel_tol])
        return False


def mse_n_ssim(file_1, file_2):
    img_1 = cv2.imread(file_1)
    img_2 = cv2.imread(file_2)
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((img_1.astype("float") - img_2.astype("float")) ** 2)
    err /= float(img_1.shape[0] * img_1.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    mse = err
    # Structural Similarity Index
    img_1_gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    img_2_gray = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(img_1_gray, img_2_gray, full=True)
    return mse, score


def to_same_size(file_ori, file_todo, file_output):
    img_ori = Image.open(file_ori)
    img_todo = Image.open(file_todo)
    width_ori, height_ori = img_ori.size
    width_todo, height_todo = img_todo.size
    width = width_ori
    height = round(height_todo * 1.0 / width_todo * width_ori)
    img_resize = img_todo.resize((width, height), Image.ANTIALIAS)
    img_resize.save(file_output)
