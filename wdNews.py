import json, re, time
from datetime import datetime
import requests
from lxml import etree

def get_clsnews():
    week = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    url = "https://www.cls.cn/api/sw?app=CailianpressWeb&os=web&sv=7.7.5"
    data = {"type": "telegram", "keyword": "你需要知道的隔夜全球要闻", "page": 0,
            "rn": 1, "os": "web", "sv": "7.7.5", "app": "CailianpressWeb"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"}
    try:
        rsp = requests.post(url=url, headers=headers, data=data)
        data = json.loads(rsp.text)["data"]["telegram"]["data"][0]
        news = data["descr"]
        timestamp = data["time"]
        ts = time.localtime(timestamp)
        weekday_news = datetime(*ts[:6]).weekday()
    except Exception as e:
        print(e)
        return ""
    weekday_now = datetime.now().weekday()
    if weekday_news != weekday_now:
        return ""
    fmt_time = time.strftime("%Y年%m月%d日", ts)
    news = re.sub(r"(\d{1,2}、)", r"\n\n\1", news)
    fmt_news = "".join(etree.HTML(news).xpath(" // text()"))
    fmt_news = re.sub(r"周[一|二|三|四|五|六|日]你需要知道的", r"", fmt_news)
    return f"{fmt_time} {week[weekday_news]}\n\n{fmt_news}"

def message_content():
    content = (
        get_clsnews() 
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
    # info_time = datetime.now()
    # news_time = datetime.strftime(info_time,"%Y%m%d")
    wxbootkey = '38f8e08a-3f62-410e-9f84-b60799673f69'
    weixin_push(message_content())
