# coding: utf-8

# 微信公众号菜单栏设置
# 公众号平台有ip白名单限制, 只能在限定ip的机器上执行

import json
import requests

wx_official_access_token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
wx_official_menu_create_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
wx_official_menu_delete_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s"


test_appid = "wx1234567890abcdef"
test_appsecret = "0123456789abcdefghijk01234567890"


test_menu = '''{
        "button": [
            {
                "type": "click",
                "name": "菜单1",
                "key": "V101_MENU1"
            },
            {
                "type": "view",
                "name": "菜单1",
                "url": "http://www.baidu.com"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "子菜单1",
                        "url": "http://www.baidu.com"
                    },
                    {
                        "type": "click",
                        "name": "子菜单2",
                        "key": "V102_MENU2"
                    }
                ]
            }
        ]
    }'''


"""
请求
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx12d8021fc
返回
{
    "access_token": "6_Fq3UOWGAGDF",
    "expires_in": 7200
}
"""
def get_wx_official_access_token(_appid, _appsecret):
    url = wx_official_access_token_url % (_appid, _appsecret)
    print url
    try:
        ret = requests.get(url)
        if ret.status_code != 200:
            print "error code %s" % str(ret.status_code)
            return None
        res = json.loads(ret.content)
        print "res %s" % str(res)
        if not res:
            return None
        if isinstance(res, dict) and  res.has_key('access_token') and res['access_token']:
            return res['access_token']
        return None
    except Exception, e:
        print "exception %s" % str(e)
        return None

"""
请求
https://api.weixin.qq.com/cgi-bin/menu/create?access_token=6_Fq3UOWGAGDF
返回
{
    "errcode": 0,
    "errmsg": "ok"
}
"""
def post_menu_wx_official():
    access_token = get_wx_official_access_token(test_appid, test_appsecret)
    payload = test_menu
    if not access_token:
        return False
    url = wx_official_menu_create_url % access_token
    print url
    ret = requests.post(url, data=payload)
    if ret.status_code != 200:
        print "error code %s" % str(ret.status_code)
        return False
    res = json.loads(ret.content)
    print "res %s" % str(res)
    if not res:
        return False
    if isinstance(res, dict) and res.has_key('errcode') and res['errcode'] == 0:
        return True
    return False


def del_menu_wx_official():
    access_token = get_wx_official_access_token(test_appid, test_appsecret)
    if not access_token:
        return False
    url = wx_official_menu_delete_url % access_token
    print url
    ret = requests.get(url)
    if ret.status_code != 200:
        print "error code %s" % str(ret.status_code)
        return False
    res = json.loads(ret.content)
    print "res %s" % str(res)
    if not res:
        return False
    if isinstance(res, dict) and 'errcode' in res and res['errcode'] == 0:
        return True
    return False


if __name__ == '__main__':
    post_menu_wx_official()
    # del_menu_wx_official()

