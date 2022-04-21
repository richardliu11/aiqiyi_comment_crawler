# 爱奇艺评论数据抓取
# -*- coding: utf-8 -*-
# Author : richard
# Date : 2022/4/21
# 抓取对象说明：爱奇艺平台某视频下评论，及评论用户信息。
# 不同视频由TVID号控制，体现在API的content_id字段。

import requests
import json
import re
import time
import pandas as pd


def pattern_return(pattern_str, html):  # 正则匹配方式
    '''
    :param pattern_str:
    :param html:
    :return:
    '''
    try:
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, html)
        if len(items) <= 1:
            items = items[0]
    except:
        items = None
    return items


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

    url = "https://sns-comment.iqiyi.com/v3/comment/get_comments.action?agent_type=118&agent_version=9.11.5&authcookie=null&business_type=17&content_id=7222400481724500&page=&page_size=40&types=time&last_id="
    url += str(lastId)
    responseTxt = getMovieinfo(url)
    responseJson = json.loads(responseTxt)
    comments = responseJson['data']['comments']  # API返回内容
    # print(comments)
    for val in comments:
        # print(val.keys())
        if 'id' in val.keys():
            id = val['id']  # 评论id
        else:
            id = None
        if 'addTime' in val.keys():
            addTime = val['addTime']  #评论时间
        else:
            addTime = None
        if 'content' in val.keys():
            content = val['content']  #评论内容
        else:
            content = None
        if 'likes' in val.keys():
            likes = val['likes']
        else:
            likes = None
        if 'userInfo' in val.keys():
            userInfo = val['userInfo']
            userInfo = [userInfo]

            for info in userInfo:
                if 'uid' in info.keys():
                    uid = info['uid']
                else:
                    uid = None
                if 'gender' in info.keys():
                    gender = info['gender']
                else:
                    gender = None
                if 'vipType' in info.keys():
                    vipTyper = info['vipType']
                else:
                    vipTyper = None



        dic = dict(
            zip(['id', 'addTime', 'content', 'likes', 'uid', 'gender', 'vipType'],
                [id,addTime,content,likes,uid,gender,vipTyper]))
        arr.append(dic)

        lastId = str(val['id'])
        # print(lastId)
    return lastId


# 评论是多分页的，得多次请求爱奇艺的评论接口才能获取多页评论,有些评论含有表情、特殊字符之类的
# num 是页数，一页10条评论，假如爬取1000条评论，设置num=100
## 转换数据
if __name__ == '__main__':
    num = 165  # 页数
    lastId = '0'
    arr = []
    for i in range(num):
        process= round(i/num*100,2)
        print('正在抓取第', i, '页', ';', '共：', num , '页',';',str(process)+'%')

        lastId = saveMovieInfoToFile(lastId, arr)
        time.sleep(5)

    # print(arr)
    arr = pd.DataFrame(arr)
    arr.to_excel("心居S01E01_comment.xlsx", index=False)
    print("共获取评论：", len(arr), '条')



