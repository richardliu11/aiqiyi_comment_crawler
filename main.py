import requests
import json
import re
import time

# 请求爱奇艺评论接口，返回response信息
def getMovieinfo(url):
    '''
        请求爱奇艺评论接口，返回response信息
        参数  url: 评论的url
        :return: response信息
    '''
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        # "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "http://m.iqiyi.com/v_19rqriflzg.html",
        "Origin": "http://m.iqiyi.com",
        "Host": "sns-comment.iqiyi.com",
        "Connection": "keep-alive",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
        "Accept-Encoding": "gzip, deflate"
                           ""
    }
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 解析json数据，获取评论
def saveMovieInfoToFile(lastId, arr):
    '''
        解析json数据，获取评论
        参数  lastId:最后一条评论ID  arr:存放文本的list

    '''

    url = "https://sns-comment.iqiyi.com/v3/comment/get_comments.action?agent_type=118&agent_version=9.11.5&authcookie=null&business_type=17&content_id=7222400481724500&page=&page_size=10&types=time&last_id="
    url += str(lastId)
    responseTxt = getMovieinfo(url)
    responseJson = json.loads(responseTxt)
    comments = responseJson['data']['comments']

    for val in comments:
        # print(val.keys())
        if 'content' in val.keys():
            print(val['content'])
            arr.append(val['content'])
        lastId = str(val['id'])
    return lastId

#使用正则去除文本中特殊字符
def clear_special_char(content):
    '''
	    正则处理特殊字符
	    参数 content:原文本
	    return: 清除后的文本
    '''
    s = re.sub(r"</?(.+?)>|&nbsp;|\t|\r",  "",content)
    s = re.compile('[a-zA-Z]')
    s = re.compile('^\d+(\.\d+)?$')
    s = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5]')
    return s.sub('', content)

#评论是多分页的，得多次请求爱奇艺的评论接口才能获取多页评论,有些评论含有表情、特殊字符之类的
#num 是页数，一页10条评论，假如爬取1000条评论，设置num=100
## 转换数据
if __name__ == '__main__':
    num=400
    lastId='0'
    arr=[]
    with open('aqy.txt', 'a', encoding='utf-8') as f:
        for i in range(num):
            lastId=saveMovieInfoToFile(lastId, arr)
            time.sleep(0.5)
        for item in arr:
            item=clear_special_char(item)
            if item.strip()!='':
                try:
                    f.write(item+'\n')
                except  :
                    print('含有特殊字符')
    print("共获取评论：", len(arr))
    f=open('aqy.txt', 'r', encoding='utf-8')
    counts={}

    file_path='aqy.txt'
    test_text=[]
