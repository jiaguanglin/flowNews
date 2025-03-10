# weibo hots
import os, requests, base64, hashlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

wkdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(wkdir)

def hot_search():
    url = 'https://weibo.com/ajax/side/hotSearch'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()['data']

def decoding(num):
    data = hot_search()
    if not data:
        print('获取微博热搜榜失败')
        return
    top = (f"置顶:{data['hotgov']['word'].strip('#')}")
    hot_li = []
    hot_label = []
    for i, rs in enumerate(data['realtime'][:num], 1):
        title = rs['word']
        try:
            label = rs['label_name']
            if label in ['热','新']:
                label = label
            else:
                label = ''
        except:
            label = ''
        # hot_li.append(f"{i}. {title} {label}")
        hot_li.append(f"{title}")
        hot_label.append(f"{label}")
    return hot_li,hot_label

def img(li,label):
    # 创建图像
    width= 750
    height = 350+ 70 + len(li)*52
    background = Image.new('RGB', (width, height), color=(255, 255, 255))
    # 添加背景图片（如果需要替代顶部像素的背景）
    background_image = Image.open('resource/hot_research.jpg')  # 替换为你的背景图片
    background.paste(background_image, (0, 0))

    line_height = 50  # 每行文字高度
    num_lines = len(li) # 总行数
    font_size = 30  # 字体大小
    text_color = (0, 0, 0)  # 文本颜色
    background_color = (255, 255, 255)  # 背景颜色
    separator_color = (200, 200, 200)  # 分隔符颜色
    separator_height = 1  # 分隔符高度
    image_height = num_lines * line_height  # 图像高度

    # 字体配置
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("resource/heiti.ttf", font_size)
    num_font = ImageFont.truetype("resource/SmileySans.ttf", font_size)
    # 生成文本列表
    lines = li
    # 获取当前时间
    wlst = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    wekd = wlst[datetime.now().weekday()]
    time = datetime.now().strftime('20%y年%m月%d日 %H:%M') +' '+wekd
    time_name = datetime.now().strftime('20%y年%m月%d日%H')
    draw.text((130, 360), str(time), fill=(101, 109, 118), font=font,font_size=24)
    draw.rectangle([(0, 400), (width, 400+ separator_height)], fill=separator_color)
    # 逐行绘制文本和分隔符
    y = 420
    i = 1
    for line in lines:
        # 绘制编号
        draw.text((35,y-3),str(i), fill=(255,0,0),font=num_font)
        # 绘制文本
        draw.text((130, y),line, fill=text_color, font=font)
        # 绘制热度
        draw.text((680, y-3), label[i-1], fill=(255,0,0), font=num_font)
        y += line_height
        i +=1
        # 绘制分隔符
        draw.rectangle([(0, y-10), (width, y-10 + separator_height)], fill=separator_color)
        y += separator_height

    # 保存图像
    try :
        background.save(f"archive/{time_name}.png")
        print("保存成功！")
    except:
        print("保存失败！！！")
        
def webHot():
    num = 25 #获取热搜数
    hot_li = decoding(num)[0]
    hot_label = decoding(num)[1]
    img(hot_li,hot_label)

def upload_image(time_name):
    img_path = f"archive/{time_name}.png"
    print(img_path)
    with open(img_path, 'rb') as f:
        image = f.read()
        img_64 = base64.b64encode(image)#, enocding='utf-8'
        img_h5 = hashlib.md5(image)
        img64 = img_64.decode('utf8')
        imgh5 = img_h5.hexdigest()
    return img64, imgh5

def weixin_push(time_name):
    img64, imgh5 = upload_image(time_name)
    payload = {
            "msgtype":"image",
            "touser":"@all",
            "image":{
                    "base64": img64,
		    "md5": imgh5
            }
        }
    resp = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s'%wxbootkey, json=payload)
    result = resp.json()

if __name__ == '__main__':
    time_name = datetime.now().strftime('20%y年%m月%d日%H')
    webHot()
    # wxbootkey = '61858489-6390-4dc8-8e1f-f58536d9fc35'
    wxbootkey = '38f8e08a-3f62-410e-9f84-b60799673f69'
    weixin_push(time_name)
