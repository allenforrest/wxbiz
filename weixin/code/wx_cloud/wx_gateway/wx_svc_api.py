#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-26
Description: 微信对外提供的服务API（由于微信私有API尚未开放，目前暂时用模拟登陆的方式实现）
Key Class&Method List: 
             1. WXServiceAPI
History:
1. Date: 2013-5-26
   Author: Allen
   Modification: create
"""
if __name__ == '__main__':
    import import_paths
    
import requests
import urllib
import mimetools
import json
import md5

import tracelog

WX_WEB_LOGIN_URL = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'

WX_WEB_GET_INFO_REFERER = 'https://mp.weixin.qq.com/cgi-bin/getmessage?t=wxm-message&lang=zh_CN&count=50&token=%s'
WX_WEB_GET_INFO_URL = 'https://mp.weixin.qq.com/cgi-bin/getcontactinfo?t=ajax-getcontactinfo&lang=zh_CN&fakeid=%s'

WX_WEB_SEND_MSG_REFERER = 'https://mp.weixin.qq.com/cgi-bin/singlemsgpage?fromfakeid=%s&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN'
WX_WEB_SEND_MSG_URL = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response'

WX_WEB_GET_SUBSCRIBERS_URL = 'https://mp.weixin.qq.com/cgi-bin/contactmanagepage?token=%s&t=wxm-friend&pagesize=100&groupid=%d'
WX_WEB_GET_SUB_LAST_MSGS_URL = 'https://mp.weixin.qq.com/cgi-bin/singlemsgpage?t=ajax-single-getnewmsg'

WX_WEB_GET_MP_INFO_URL = 'https://mp.weixin.qq.com/cgi-bin/userinfopage?t=wxm-setting&token=%s&lang=zh_CN'

WX_WEB_UPLOAD_IMG_URL = "https://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&type=2&token=%s&t=iframe-uploadfile&lang=zh_CN&formId=1"
WX_WEB_UPLOAD_IMG_REFERER = 'https://mp.weixin.qq.com/cgi-bin/indexpage?token=%s&t=wxm-upload&lang=zh_CN&type=2&formId=1'

WX_WEB_CREATE_NEWS_URL = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&t=ajax-response&sub=create'
WX_WEB_CREATE_NEWS_REFERER = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=edit&t=wxm-appmsgs-edit-new&type=10&subtype=3&lang=zh_CN'

WX_WEB_DEL_NEWS_URL = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=del&t=ajax-response'
WX_WEB_DEL_NEWS_REFERER = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=%s&lang=zh_CN&sub=list&type=10&subtype=3&t=wxm-appmsgs-list-new&pagesize=10&pageidx=0&lang=zh_CN'

WX_WEB_DEL_IMG_URL = 'https://mp.weixin.qq.com/cgi-bin/modifyfile?oper=del&lang=zh_CN&t=ajax-response'
WX_WEB_DEL_IMG_REFERER = 'https://mp.weixin.qq.com/cgi-bin/filemanagepage?t=wxm-file&lang=zh_CN&token=%s&type=2&pagesize=10&pageidx=0'

WX_WEB_ITF_CFG_INFO_MOD_URL = 'https://mp.weixin.qq.com/cgi-bin/callbackprofile?t=ajax-response&lang=zh_CN'
WX_WEB_ITF_CFG_INFO_MOD_REFERER = 'https://mp.weixin.qq.com/cgi-bin/devapply?opcode=getinfo&t=wxm-developer-api-reg-port&token=%s&lang=zh_CN'

WX_WEB_ITF_CFG_INFO_GET_URL = 'https://mp.weixin.qq.com/cgi-bin/operadvancedfunc?op=list&t=wxm-developer-api&token=%s&lang=zh_CN'

WX_WEB_GET_WAN_IP_URL = 'http://ip5.me'

class WXServiceAPI(object):

    def __init__(self, username, pwd):
        self._username = username
        self._pwd = md5.md5(pwd).hexdigest()
        self._token = None
        self._biz_fakeid = None
        self._requests_session = None
        self._login_succ = False
    
    def _login(self):
        self._requests_session = requests.session()
        self._requests_session.cookies.clear_session_cookies()
        param = {}
        param['username'] = self._username
        param['pwd'] = self._pwd
        param['f'] = 'json'
        
        resp = self._requests_session.get(WX_WEB_LOGIN_URL, verify = True, params = param)
        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            err_msg = resp_json['ErrMsg']
            self._token = err_msg[err_msg.find('token=') + 6:]
            
            tracelog.info('WX Biz(%s) login succ!' % self._username)
            self._login_succ = True
            return True
        else:
            return False        
        
    def get_biz_fakeid(self):
        if self._login_succ is False:
            self._login()
            
        url = WX_WEB_GET_MP_INFO_URL % self._token
        resp = self._requests_session.get(url, verify = True)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
            
            spos = resp.text.find(' FakeID   : "') + len(' FakeID   : "')
            epos = resp.text.find('"', spos)            
            self._biz_fakeid = resp.text[spos: epos]
            return self._biz_fakeid
        else:
            return ''    
    
    def get_subscribers_by_group(self, group):
        if self._login_succ is False:
            self._login()
        
        url = WX_WEB_GET_SUBSCRIBERS_URL % (self._token, group)
        resp = self._requests_session.get(url, verify = True)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
                        
            # [{"fakeId" : "", "nickName": "", "remarkName": "", "groupId" : "0"}, ... ]
            spos = resp.text.find('<script id="json-friendList" type="json/text">') + len('<script id="json-friendList" type="json/text">')
            epos = resp.text.find('</script>', spos)
            sub_list_str = resp.text[spos: epos]
            return sub_list_str
        else:
            return ''            
    
    def get_subscriber_info(self, fakeid):
        if self._login_succ is False:
            self._login()

        param = {}
        param['ajax'] = 1
        param['token'] = self._token
        header = {'Referer': WX_WEB_GET_INFO_REFERER % self._token}                        
        resp = self._requests_session.post(WX_WEB_GET_INFO_URL % fakeid, verify = True, params = param, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
                        
            # {FakeId:100001, NickName:'', Username:'', Signature:'', Country:'', Province:'', City:'', Sex:'1', GroupID:'0', Groups:[...]}
            return resp.text
        else:
            return ''            
        
    def get_subscriber_avatar(self, fakeid):
        if self._login_succ is False:
            self._login()
                
    def get_subscriber_last_msgs(self, fakeid):
        if self._login_succ is False:
            self._login()

        param = {}
        param['fromfakeid'] = fakeid
        param['opcode'] = 1
        param['token'] = self._token
        param['ajax'] = 1
            
        resp = self._requests_session.post(WX_WEB_GET_SUB_LAST_MSGS_URL, verify = True, params = param)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
                        
            # [{"fileId":"0","source":"biz","fakeId":"2396330532","hasReply":"0","nickName":"","dateTime":"1369578681","icon":"","content":"test&nbsp;push&nbsp;msg","playLength":"0","length":"0","starred":"0","status":"2","subtype":"0","showType":"0","desc":"","title":"","appName":"","contentUrl":"","bcardNickName":"","bcardUserName":"","bcardFakeId":"0","id":"367","type":"1"},...]
            return resp.text
        else:
            return ''            
        
    def send_text(self, fakeid, text):
        if self._login_succ is False:
            self._login()
        
        param = {}
        param['tofakeid'] = fakeid
        param['type'] = 1
        param['token'] = self._token
        param['content'] = text
        param['ajax'] = 1
        header = {'Referer': WX_WEB_SEND_MSG_REFERER % self._biz_fakeid}                        
        resp = self._requests_session.post(WX_WEB_SEND_MSG_URL, verify = True, params = param, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
                        
            # {"ret":"0", "msg":"ok"}
            return resp.text
        else:
            return ''            
    
    def send_news(self, fakeid, news_id):
        if self._login_succ is False:
            self._login()
        
        param = {}
        param['tofakeid'] = fakeid
        param['type'] = 10
        param['token'] = self._token
        param['content'] = ''
        param['fid'] = news_id
        param['appmsgid'] = news_id
        param['error'] = False
        param['ajax'] = 1
        header = {'Referer': WX_WEB_SEND_MSG_REFERER % self._biz_fakeid}                        
        resp = self._requests_session.post(WX_WEB_SEND_MSG_URL, verify = True, params = param, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
            
            # {"ret":"0", "msg":"ok"}
            return resp.text
        else:
            return ''

    def _upload_img(self, file_name):
        if self._login_succ is False:
            self._login()

        try:
            ff = open(file_name, 'rb')
            file_buf = ff.read()
            ff.close()
        except Exception, e:
            tracelog.error('open file %s exceptional(%s)' % (file_name, e))
            return None
            
        CRLF = '\r\n'
        boundary = mimetools.choose_boundary()
        lines = []
        lines.append('-----------------------------%s' % boundary)
        lines.append('Content-Disposition: form-data; name="uploadfile"; filename="%s"' % file_name)
        lines.append('Content-Type: image/jpeg')
        lines.append('')
        lines.append(file_buf)
        lines.append('-----------------------------%s' % boundary)
        lines.append('Content-Disposition: form-data; name="formId"')
        lines.append('')
        lines.append('-----------------------------%s--' % boundary)
        
        body = CRLF.join(lines)
        
        header = {'Referer': WX_WEB_UPLOAD_IMG_REFERER % self._token,
                  'Content-Type': 'multipart/form-data; boundary=---------------------------%s' % boundary,
                  'Content-Length': '%s' % len(body)
                   }                        

        resp = self._requests_session.post(WX_WEB_UPLOAD_IMG_URL % self._token, verify = True, data = body, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
            buf = resp.text
            s = buf.find('type, formId, ') + len('type, formId, ')
            e = buf.find(')', s)
            file_id = buf[s:e].strip("'")            
            return file_id
        else:
            tracelog.error('upload img failed(status code %d)' % resp.status_code)
            return None

    def _del_img(self, img_id):
        if self._login_succ is False:
            self._login()

        params = {}
        params['fileid'] = img_id
        params['token'] = self._token
        params['ajax'] = 1
        body = urllib.urlencode(params)
        header = {'Referer': WX_WEB_DEL_IMG_REFERER % self._token}
        
        resp = self._requests_session.post(WX_WEB_DEL_IMG_URL, verify = True, data = body, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return False
            
            # {"ret":"0", "msg":"ok"}
            ret_json = json.loads(resp.text)
            if ret_json['ret'] == "0":
                return True
            else:
                tracelog.error('del news OK, ret error(%s)' % resp.text)
                return False                
        else:
            tracelog.error('del news failed(status code %d)' % resp.status_code)
            return False   
    
    def del_news(self, news_id):
        if self._login_succ is False:
            self._login()
            
        self._del_img(str(int(news_id) - 1))
        
        params = {}
        params['AppMsgId'] = news_id
        params['token'] = self._token
        params['ajax'] = 1
        body = urllib.urlencode(params)
        header = {'Referer': WX_WEB_DEL_NEWS_REFERER % self._token}
        
        resp = self._requests_session.post(WX_WEB_DEL_NEWS_URL, verify = True, data = body, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return False
            
            # {"ret":"0", "msg":"ok"}
            ret_json = json.loads(resp.text)
            if ret_json['ret'] == "0":
                return True
            else:
                tracelog.error('del news OK, ret error(%s)' % resp.text)
                return False                
        else:
            tracelog.error('del news failed(status code %d)' % resp.status_code)
            return False         
        

    def create_news(self, pic_file_name, back_pic_file_name, title, desc, content):
        if self._login_succ is False:
            self._login()
        
        img_id = self._upload_img(pic_file_name)
        if img_id is None or img_id.isdigit() is False:
            tracelog.error('upload img failed, reupload the default logo img')
            img_id = self._upload_img(back_pic_file_name)
            if img_id is None or img_id.isdigit() is False:
                tracelog.error('upload the default logo img fail!')
                return None
        
        params = {}
        params['fileid0'] = img_id
        params['content0'] = content
        params['digest0'] = desc
        params['token'] = self._token
        params['title0'] = title
        params['AppMsgId'] = ''
        params['count'] = 1
        params['error'] = False
        params['ajax'] = 1
        body = urllib.urlencode(params)

        header = {'Referer': WX_WEB_CREATE_NEWS_REFERER % self._token}
        
        resp = self._requests_session.post(WX_WEB_CREATE_NEWS_URL % self._token, verify = True, data = body, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
            
            # {"ret":"0", "msg":"ok"}
            ret_json = json.loads(resp.text)
            if ret_json['ret'] == "0":
                return str(int(img_id) + 1)
            else:
                tracelog.error('create news OK, ret error(%s)' % resp.text)
                return None                
        else:
            tracelog.error('create news failed(status code %d)' % resp.status_code)
            return None         

    def get_itf_cfg_info(self):
        if self._login_succ is False:
            self._login()
        
        resp = self._requests_session.get(WX_WEB_ITF_CFG_INFO_GET_URL % self._token, verify = True)
        if resp.status_code == 200:
            prefix = '<dd class="dev_tip"><label>URL：</label><strong>'
            s = resp.text.find(prefix) + len(prefix) - 1
            e = resp.text.find('</strong></dd>', s)
            itf_cfg_url = resp.text[s:e]
            return itf_cfg_url
        else:
            return None  
                

    def mod_itf_cfg_info(self, url, access_token):
        if self._login_succ is False:
            self._login()
        
        params = {}
        params['url'] = url
        params['callback_token'] = access_token
        params['token'] = self._token
        params['ajax'] = 1
        body = urllib.urlencode(params)

        header = {'Referer': WX_WEB_ITF_CFG_INFO_MOD_REFERER % self._token}
        
        resp = self._requests_session.post(WX_WEB_ITF_CFG_INFO_MOD_URL, verify = True, data = body, headers = header)
        if resp.status_code == 200:
            if len(resp.text) == 1614:
                self._login_succ = False
                return None
            
            # {"ret":"0", "msg":token}
            ret_json = json.loads(resp.text)
            if ret_json['ret'] == "0" and ret_json['msg'] == self._token:
                return True
            else:
                tracelog.error('mod itf cfg info OK, ret error(%s)' % resp.text)
                return False                
        else:
            tracelog.error('mod itf cfg info failed(status code %d)' % resp.status_code)
            return False
        
    def get_wan_ip(self):
        resp = self._requests_session.get(WX_WEB_GET_WAN_IP_URL)
        if resp.status_code == 200:
            prefix = '<input name="s" size="60" value="'
            s = resp.text.find(prefix) + len(prefix)
            e = resp.text.find('"', s)
            wan_ip = resp.text[s:e]
            return wan_ip
        else:
            return None         


if __name__ == '__main__':
    wx_api = WXServiceAPI('allenxu@gmail.com', 'Xuweinan812185')
    
    print 'my fakeid %s, token %s' % (wx_api.get_biz_fakeid(), wx_api._token)
    
    print wx_api.get_itf_cfg_info()
    
    """
    subs = wx_api.get_subscribers_by_group(0)
    print subs
    
    sub_list = json.loads(subs)
    for sub in sub_list:
        print 'sub fakeid %s, nick %s' % (sub['fakeId'], sub['nickName'])
        last_msg = wx_api.get_subscriber_last_msgs(sub['fakeId'])
        print last_msg
        lmo = json.loads(last_msg)
        for l in lmo:
            print l['content']
            print l['content'].encode('utf-8').find('您是第'.decode('gbk').encode('utf-8'))
    
    #news_id = wx_api.create_news('1.jpg', 'xuweinan1', 'xuweinan1 create', 'hello world1')
    #print news_id
    
    #print wx_api.del_news('10000043')
    """
    #wx_api.mod_itf_cfg_info('http://whatsnfc.sinaapp.com/weixin', 'allenforrest')