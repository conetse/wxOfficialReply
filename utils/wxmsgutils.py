# coding: utf-8

import time
import xml.etree.ElementTree as ET
from utils.wxMsgCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from config.wx_config import example_app_winxin_token, example_encodingAESKey, example_appid

example_wx_cryp_tool = WXBizMsgCrypt(example_app_winxin_token, example_encodingAESKey, example_appid)

def parse_wx_msg_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextRMsg(xmlData)
    elif msg_type == 'image':
        return ImageRMsg(xmlData)
    elif msg_type == 'location':
        return LocationRMsg(xmlData)
    elif msg_type == 'event':
        return EventRMsg(xmlData)

class Event(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.Event = xmlData.find('Event').text

class RMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class TextRMsg(RMsg):
    def __init__(self, xmlData):
        RMsg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageRMsg(RMsg):
    def __init__(self, xmlData):
        RMsg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class LocationRMsg(RMsg):
    def __init__(self, xmlData):
        RMsg.__init__(self, xmlData)
        self.Location_X = xmlData.find('Location_X').text
        self.Location_Y = xmlData.find('Location_Y').text

class EventRMsg(Event):
    def __init__(self, xmlData):
        Event.__init__(self, xmlData)
        self.Eventkey = xmlData.find('EventKey').text


class TMsg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"

class TextTMsg(TMsg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class ImageTMsg(TMsg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class NewsTMsg(TMsg):
    def __init__(self, toUserName, fromUserName, news_data):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Title1'] = news_data['title']
        self.__dict['Description1'] = news_data['description']
        self.__dict['PicUrl1'] = news_data['picUrl']
        self.__dict['Url1'] = news_data['url']

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
            <item>
                <Title><![CDATA[{Title1}]]></Title>
                <Description><![CDATA[{Description1}]]></Description>
                <PicUrl><![CDATA[{PicUrl1}]]></PicUrl>
                <Url><![CDATA[{Url1}]]></Url>
            </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)


def genReplyTMsg(toUserName, fromUserName, replyData, replyType):
    if not replyData:
        return None
    if replyType == 'text':
        replyMsg = TextTMsg(toUserName, fromUserName, replyData)
    elif replyType == 'news':
        replyMsg = NewsTMsg(toUserName, fromUserName, replyData)
    else:
        replyMsg = None
    return replyMsg


def wx_msg_encrypt(to_xml, nonce):
    cryp_tool = example_wx_cryp_tool
    ret, encrypt_xml = cryp_tool.EncryptMsg(to_xml, nonce)
    return ret, encrypt_xml


def wx_msg_decrypt(from_xml, msg_sign, timestamp, nonce):
    cryp_tool = example_wx_cryp_tool
    ret, decryp_xml = cryp_tool.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
    return ret, decryp_xml

