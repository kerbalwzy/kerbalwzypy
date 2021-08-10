# -*- coding:utf-8 -*-
# @Author: wzy
# @Time: 2021/3/18
# 二维码工具函数
import os
from io import BytesIO
import base64
# 依赖第三方包 qrcode
import qrcode
# 依赖第三方包 pillow
from PIL import Image, ImageDraw, ImageFont
# 依赖第三方包 pyzbar
from pyzbar import pyzbar

from u_string import contains_chinese

__all__ = ['create_qr_code', 'qr_code_parser']

FONT_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/fonts/arial.ttf")


def create_qr_code(text: str, logo: str = None, note: str = None):
    """
    创建二维码, 并返回二维码图片的base64字符串
    :param text: 二维码内容
    :param logo: 二维码中间logo图片
    :param note: 水印备注, 最多只会写入32个ASCII码字符, 不支持输入中文, 显示在二维码外部左上角
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=14,
        border=4,
    )
    # 添加数据
    qr.add_data(text)
    # 填充数据
    qr.make(fit=True)
    # 生成图片
    img = qr.make_image(fill_color="#000", back_color="#FFF")
    if logo:
        # 添加logo，打开logo照片
        icon = Image.open(logo)
        # 获取图片的宽高
        img_w, img_h = img.size
        # 参数设置logo的大小
        factor = 5
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        # 重新设置logo的尺寸
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        # 得到画图的x，y坐标，居中显示
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        # 黏贴logo照
        img.paste(icon, (w, h), mask=None)
    if note and not contains_chinese(note):
        note = note[:32]
        font = ImageFont.truetype(FONT_FILE_PATH, 19)
        draw = ImageDraw.Draw(img)
        draw.text((56, 20), note, (0, 0, 0), font=font)
    # img.show()
    # 创建内存文件对象
    f = BytesIO()
    img.save(f)
    f.seek(0)
    bytes_data = f.read()
    f.close()
    return base64.b64encode(bytes_data).decode()


def qr_code_parser(image):
    img = Image.open(image)
    instance = pyzbar.decode(img)
    content = ""
    for barcode in instance:
        content += barcode.data.decode("utf-8")
        if barcode.type != "QRCODE":
            return None
    return content
