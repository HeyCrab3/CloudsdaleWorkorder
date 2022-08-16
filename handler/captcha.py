import string
from io import BytesIO
import random
from PIL import Image, ImageFont, ImageDraw
from flask import Blueprint, session, make_response

bp = Blueprint('captcha', __name__)
def geneText():
    '''生成4位验证码'''
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    characters = random.sample(alphabet, 4)
    return ''.join(characters)
def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
def getVerifyCode():
    '''生成验证码图形'''
    code = geneText()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype('app/static/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=rndColor(), font=font)
    return im, code
@bp.route('/api/verify/captcha')
def captcha():
    image, code = getVerifyCode()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['imageCode'] = code
    return response