# cn news
import re, datetime
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4651.0 Safari/537.36'
}

# craw news
def get_hanlder(url):
    try:
        rsp = requests.get(url, headers=headers, timeout=5)
        rsp.raise_for_status()
        rsp.encoding = rsp.apparent_encoding
        return rsp.text
    except requests.RequestException as error:
        print(error)
        exit()

def get_news():
    strTime = (datetime.date.today() + datetime.timedelta(hours=8)).strftime("%Y%m%d")
    url = f'https://tv.cctv.com/lm/xwlb/day/{strTime}.shtml'
    rsp = get_hanlder(url)
    etr = etree.HTML(rsp)
    titles = etr.xpath("//li/a/text()")
    hrefs = etr.xpath("//li/a/@href")

    news = ''
    summary = None
    for title, href in zip(titles, hrefs):
        if '《新闻联播》' in title:
            # get abstracts
            title_rsp = get_hanlder(href)
            summary = re.search(r'<div class="video_brief">本期节目主要内容：[\s\S]*。', title_rsp).group(0).replace('<div class="video_brief">', "")
            news = news + summary
            continue
    return news
    
def message_content(news_time):
    cn_news = get_news()
    content = (
        news_time + "\n\n"
        "【新闻联播】\n\n"+
        str(cn_news)
    )
    return content

def weixin_push(content):
    wx_push_data = {
            "msgtype":"text",
            "touser":"@all",
            "text":{
                    "content":content
            },
            "safe":0
        }
    resp = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s'%wxbootkey,json=wx_push_data)
    result = resp.json()
    if result["errcode"] == 0:
        print("消息发送成功")
    else:
        print(result)

if __name__ == '__main__':
    news_time = (datetime.date.today() + datetime.timedelta(hours=8)).strftime("%Y年%m月%d日")
    wxbootkey = '38f8e08a-3f62-410e-9f84-b60799673f69'
    weixin_push(message_content(news_time))
