# coding: utf-8

def has_any_keys(content, keys, ignoreCase=True):
    try:
        _content = content.lower()
        if isinstance(keys, str):
            if _content.find(keys) >= 0:
                return True
        elif isinstance(keys, list) and len(keys) > 0:
            for k in keys:
                if _content.find(k) >= 0:
                    return True
            return False
    except Exception as e:
        print("err %s" % str(e) )
        return False
    return False



class WxOfficialReplyModule(object):

    def __init__(self):
        pass

    def reply_text(self, content):
        try:
            if content == '1':
                news_data = wx_official_reply_articles['news_test']
                return 'news', news_data
            elif content == '2':
                return 'text', wx_official_reply_texts['V102_MENU2']
            elif content == '你好':
                news_data = wx_official_reply_articles['news_data1']
                return 'news', news_data
            elif has_any_keys(content, ['粉丝', '关注', '踩']):
                news_data = wx_official_reply_articles['news_data1']
                return 'news', news_data
            elif has_any_keys(content, ['有人', '客服', '人工']):
                return 'text', wx_official_reply_texts['V101_MENU1']
        except Exception as e:
            print("reply_text err %s" % str(e) )
            return 'text', None
        return 'text', None

    def reply_click(self, event_key):
        if event_key == 'V101_MENU1':
            news_data = wx_official_reply_articles['V101_MENU1']
            return 'news', news_data
        elif event_key == 'V102_MENU2':
            return 'text', wx_official_reply_texts['V102_MENU2']
        return 'text', None


wx_official_reply_texts = {
    'V101_MENU1': '很好玩吗,老是输入关键字 \n试问有哪个程序员没被要求过帮忙修修电脑、帮忙看看网络',
    'V102_MENU2': '合作联系方式：name@youremailsite.com',
}


wx_official_reply_articles = {
    'news_test': {
        'title': '“你是程序员，帮我修个电脑吧” “不会，滚”',
        'description': '试问有哪个程序员没被要求过帮忙修修电脑、帮忙看看网络怎么了？',
        'picUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/vPaN52Au6NicPYJQ4V9TedzL9pVenDOJ6KOngvA3jS1YBgyicSvhEETNiaSxLaJLFEkgaxuQejB2vvrdxgztGWaWA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1',
        'url': 'https://mp.weixin.qq.com/s/sRAVP8aYQT9oTSa4WA5lYQ',
    },
    'news_data1': {
        'title': '猜想亚马逊家用机器人五大功能 情商堪比人类',
        'description': '猜想亚马逊家用机器人五大功能 ...',
        'picUrl': 'https://mmbiz.qpic.cn/mmbiz_jpg/ow6przZuPIEUmVlfIgj1WQRlZK496AyQ4AFqP3icqtICYaQPH0hkFhrTt8RnMWN9C5iaBc5WLsrrjckibEF4FPibwQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1',
        'url': 'https://mp.weixin.qq.com/s/Kohyv9R-PyJqQmWTc7B1dg',
    },
}

