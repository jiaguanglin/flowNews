import requests, datetime
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

def get_zakers():
    r = requests.get('http://www.myzaker.com/', headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    hotpoint = soup.find_all('a', attrs={'class': 'carousel'})
    article = soup.find_all('div', attrs={'class': 'article-wrap'})
    src = soup.find_all('div', attrs={'class': 'article-footer'})
    newslist =''
    summary = None
    flag = 1
    for a in hotpoint:
        summary = '%d、' % flag + a['title'] + '\n\n'
        newslist = newslist + summary 
        flag += 1
    for i in range(0, len(article)):
        summary = '%d、' % flag + article[i].a['title'] + '\t来源：' + src[i].a['title'] + '\n\n'
        newslist = newslist + summary
        flag += 1
    # print(newslist)
    return newslist

def message_content(news_time):
    zaker_news = get_zakers()
    content = (
        news_time + "\n\n"
        "【ZAKER新闻】\n\n"+
        str(zaker_news)
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
    news_time = (datetime.datetime.now()).strftime("%Y年%m月%d日 %H时")
    # wxbootkey = '61858489-6390-4dc8-8e1f-f58536d9fc35'
    wxbootkey = '38f8e08a-3f62-410e-9f84-b60799673f69'
    weixin_push(message_content(news_time))
