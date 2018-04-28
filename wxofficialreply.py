# coding: utf-8

from gevent import monkey
monkey.patch_all()
from gevent import pywsgi

from flask import Flask
from controller.wxofficial import test_func, test_asyn
from controller.wxofficial import WxOfficalReply
from config import wx_config

app = Flask(__name__)

app.add_url_rule('/testsyn', view_func=test_func, methods=['GET', 'POST'])
app.add_url_rule('/testasyn', view_func=test_asyn, methods=['GET'])
app.add_url_rule('/wxofficial/weixin', view_func=WxOfficalReply, methods=['GET', 'POST'])

server_host = wx_config.server_host
server_port = wx_config.server_port

# flask development server
def run_flask():
    app.run(host=server_host, port=server_port)

def run_server():
    server = pywsgi.WSGIServer((server_host, server_port), app)
    server.serve_forever()

if __name__ == '__main__':
    run_server()

# python wxofficialreply.py
