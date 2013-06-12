#coding=gbk

import import_paths

from bottle import *
import bundleframework as bf
import hashlib
import threading

import cmd_code_def
import msg_params_def
    
webapp = Bottle()

class BottleThread(threading.Thread):
    def __init__(self):
        """
        Method: __init__
        Description: 线程初始化
        Parameter: 
            app: bf.BasicApp
            port_num: 端口号
        Return: 无    
        Others: 
        """

        threading.Thread.__init__(self)

    def run(self):
        """
        Method: run
        Description: soap服务端配置，运行
        Parameter: 无
        Return: 无
        Others: 
        """
        debug(True)
        run(app = webapp, host='42.121.106.242', port = 80, reloader = True)

    

class WXWebApp(bf.BasicApp):    
    """
    Class: WXWebApp
    Description: 
    Base: bf.BasicApp
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: WXWebApp 的初始化
        Parameter: 无
        Return: 
        Others: 
        """
        
        bf.BasicApp.__init__(self, "WXWebApp")
    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 
        Parameter: 无
        Return: 
        Others: 
        """

        bf.BasicApp._ready_for_work(self)

        self._bottle_thread = BottleThread()
        self._bottle_thread.start()
        
        return 0     


app = WXWebApp()

@webapp.get("/")
def get_root():
    return "bottle OK"

@webapp.post("/weixin")
def wx_access():
    wx_msg = request.body.read()
    print "req from WX: %s" % wx_msg
    frame = bf.AppFrame()
    frame.set_cmd_code(cmd_code_def.WX_ACCESS_HTTP_POST_FORWARD)
    frame.set_receiver_pid(app.get_pid("WXGateApp"))
    content = msg_params_def.CommonContentReq()
    content.init_all_attr()
    content.user_session = ''
    content.content = wx_msg
    frame.add_data(content.serialize())
    
    ack_frame = bf.rpc_request(frame, 5)

    buf = ack_frame[0].get_data()
    rpl = msg_params_def.CommonContentRsp.deserialize(buf)
    print 'ack from cloud: %s' % rpl

    return rpl.content

@webapp.get("/weixin")
def wx_auth():
    token = "liuhaiqing"
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    print "signature %s" % signature
    print "timestamp %s" % signature
    print "nonce %s" % nonce
    print "echostr %s" % echostr
    
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    print "calc hash %s" % hashstr
    if hashstr == signature:
        return echostr
    else:
        return None     
        
if __name__ == '__main__':
    app.run()

