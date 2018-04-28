# coding: utf-8
from gevent import monkey
monkey.patch_all()

import time
import datetime
import hashlib
from flask import request
from module.wxmsg import WxOfficialReplyModule
from utils import wxmsgutils
from config.wx_config import example_app_winxin_token


WX_RESP_FAIL = "fail"
WX_RESP_SUCCESS = "success"


def get_now_time_str():
    now = datetime.datetime.now()
    timeStr = now.strftime("%Y-%m-%d %H:%M:%S")
    return timeStr, now

# @app.route("/test", methods=['GET', 'POST'])
def test_func():
    sign = request.args.get("sign", "")
    if sign != "testsign":
        return
    timeStr, _ = get_now_time_str()
    if request.method == 'POST':
        return "this is response for post at " + timeStr
    else:
        return "this is response for get at " + timeStr

def test_asyn():
    sign = request.args.get("sign", "")
    if sign != "testsign":
        return
    if request.method == 'GET':
        time.sleep(2)
        timeStr, _ = get_now_time_str()
        return 'hello asyn at ' + timeStr


def WxOfficalReply():
    if request.method == "GET":
        return WxOfficalReply_GET()
    elif request.method == "POST":
        return WxOfficalReply_POST()

def WxOfficalReply_GET():
    sig = request.args.get('signature', '')
    echostr = request.args.get('echostr', '')
    nonce = str(request.args.get('nonce', ''))
    timestamp_str = str(request.args.get('timestamp', ''))
    if not sig or not echostr or not nonce or not timestamp_str:
        return WX_RESP_FAIL
    tmpLis = [example_app_winxin_token, timestamp_str, nonce]
    tmpLis.sort()
    tmpStr = ''.join(tmpLis)
    if tmpStr == '':
        return WX_RESP_FAIL
    sha = hashlib.sha1()
    sha.update(tmpStr)
    _sig = sha.hexdigest()
    if _sig != sig:
        print('_sig %s, sig %s' % (_sig, sig) )
        return WX_RESP_FAIL
    return echostr

def WxOfficalReply_POST():
    msg_sign = request.args.get('msg_signature', None)
    timestamp = request.args.get('timestamp', None)
    nonce = request.args.get('nonce', None)
    if not msg_sign or not timestamp or not nonce:
        return WX_RESP_SUCCESS
    try:
        raw_body_data = request.get_data()
        crypt_err, decryp_xml = wxmsgutils.wx_msg_decrypt(raw_body_data, msg_sign, timestamp, nonce)
        if crypt_err != 0:
            print("dec wx msg err %s" % str(crypt_err) )
            return WX_RESP_SUCCESS
        recMsg = wxmsgutils.parse_wx_msg_xml(decryp_xml)
        if isinstance(recMsg, wxmsgutils.RMsg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            if recMsg.MsgType == 'text':
                replyType, replyData = WxOfficialReplyModule().reply_text(recMsg.Content)
                replyMsg = wxmsgutils.genReplyTMsg(toUser, fromUser, replyData, replyType)
                if replyMsg:
                    send_xml = replyMsg.send()
                    crypt_err, encryp_xml = wxmsgutils.wx_msg_encrypt(send_xml, nonce)
                    if crypt_err != 0:
                        print("enc wx msg err %s" % str(crypt_err) )
                        return WX_RESP_SUCCESS
                    return encryp_xml
        else:
            print("unknown wx msg %s" % str(recMsg))
    except Exception as e:
        print("deal wx msg err %s" % str(e), 'error')
        return WX_RESP_SUCCESS
    return WX_RESP_SUCCESS

