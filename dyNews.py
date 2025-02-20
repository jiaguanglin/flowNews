import json, re, time
from datetime import datetime
import requests
from lxml import etree

def tiny_url(long_url):
    # Adf.ly Bit.ly Chilp.it Clck.ru Cutt.ly Da.gd Git.io
    # Is.gd NullPointer Os.db Ow.ly Po.st Qps.ru Short.cm Tiny.cc
    time.sleep(1)
    # tiny_url = ps.Shortener().clckru.short(long_url)
    tiny_url = ps.Shortener().osdb.short(long_url)    
    return tiny_url
   
def get_sinanews(news_type,news_time):
    news_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "top.news.sina.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://news.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
    }
    news_url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=%s&top_time=%s&top_show_num=20&top_order=DESC&js_var=news_'%(news_type,news_time)
    news_req = requests.get(url=news_url,headers=news_headers).text.replace("var news_ = ","").replace(r"\/\/","//").replace(";","")
    format_news = json.loads(json.dumps(news_req ,ensure_ascii=False))
    news_sub = json.loads(format_news)['data']
    news_list = []
    for item in news_sub:
        if str(item['url']).split(".")[0] == "https://video":
            continue
        else:
            # long_url = item['url']
            # st_url = tiny_url(long_url)
            news = item['title'] + ' 详情<%s>'%item['url']
            # news = item['title'] + ' 详情<%s>'%st_url
            news_list.append(news) 
    return news_list

def get_jinbanews():
    url = "https://www.jinrongbaguanv.com/jinba/index_articles/1"
    r=requests.get(url)
    if (r.status_code == 200):
        jsonData = json.loads(r.content)
        topics = jsonData['body']['datas']
        news_list = ''
        cunts = 0
        for topic in topics:
            cunts = cunts + 1
            # long_url = "https://m.jinrongbaguanv.com/details/details.html?id=%s"%topic['id']
            # st_url = tiny_url(long_url)
            if cunts <= 5:
                result = topic['title']
                news_list = news_list + '\n '
                news_list = news_list + str(cunts) +"、"+ result + '\n '
                # news_list = news_list + '详情<%s>'%st_url
                news_list = news_list + '详情<"https://m.jinrongbaguanv.com/details/details.html?id=%s">'%topic['id']
                news_list = news_list + '\n '
            else:
                break
    return news_list 

def get_sentence():
    sen_url = 'https://v1.hitokoto.cn?c=d&c=h&c=i&c=k'
    get_sen = requests.get(url=sen_url).json()
    sentence = get_sen['hitokoto']+"\n\n出自：%s"%get_sen['from']
    return sentence

def message_content(news_time):
    sina_china = get_sinanews('news_china_suda',news_time)
    content = (
        "【国内时政】\n\n"+
        str(sina_china[0:6]).replace("['","").replace("', '",'\n\n').replace("']",'\n')+"\n"+
        "【金八传媒】\n"+
        str(get_jinbanews()) +"\n\n"+
        "【每日一句】\n\n"+
        get_sentence()
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
    info_time = datetime.now()
    news_time = datetime.strftime(info_time,"%Y%m%d")
    wxbootkey = '61858489-6390-4dc8-8e1f-f58536d9fc35'
    weixin_push(message_content(news_time))
