from flask_babel import _
from flask import current_app
#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import urllib
import random
import json

def translate(text, source_language, dest_language):
    if 'BAIDU_TRANSLATOR_APPID' not in current_app.config or \
            'BAIDU_TRANSLATOR_SECRETKEY' not in current_app.config:
        return _('Error: the translation service is not configured.')
    appid = current_app.config['BAIDU_TRANSLATOR_APPID']
    secretKey = current_app.config['BAIDU_TRANSLATOR_SECRETKEY']  # 填写你的密钥
    
    httpClient = None
    myurl = '/api/trans/vip/translate'
    
    #fromLang = 'auto'   #原文语种
    fromLang = source_language   #原文语种
    toLang = dest_language   #译文语种
    salt = random.randint(32768, 65536)
    q = text
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
    
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
    
        print (result)
        total_str = ''
        for i in result['trans_result']:
            total_str = i['dst'] + '\n'
        total_str = total_str.strip()
        print (total_str)
        return total_str
    
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()
