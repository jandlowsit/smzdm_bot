"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests
import os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat
import json


class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            return True
        except Exception as e:
            print(f'Error : {e}')
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        cookies = cookies.encode("utf-8").decode("latin1")
        self.session.headers['Cookie'] = cookies

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return self.msgFormat(msg.json())
        return msg.content

    def msgFormat(self, msg):
        if type(msg) == "list":
            return msg

        s = msg.get("data")
        _res = "当前积分："+str(s.get("point"))+"\n"
        _res += "当前经验值："+str(s.get("exp"))+"\n"
        _res += "签到天数："+str(s.get("checkin_num"))+"\n"
        return _res


if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    sb.load_cookie_str(cookies)
    # SERVERCHAN_SECRETKEY = config.SERVERCHAN_SECRETKEY

    res = sb.checkin()
    push_to_wechat(text='什么值得买每日签到',
                   desp=str(res),
                   secretKey=SERVERCHAN_SECRETKEY)
