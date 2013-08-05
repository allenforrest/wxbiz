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
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import tracelog

WINDELN_URL = 'http://www.windeln.de'
WINDELN_LOGIN_URL = 'https://www.windeln.de/customer/account/loginPost/referer/aHR0cHM6Ly93d3cud2luZGVsbi5kZS9jdXN0b21lci9hY2NvdW50L2luZGV4Lw,,'
WINDELN_LOGIN_REFERER = 'https://www.windeln.de/customer/account/login/referer/aHR0cHM6Ly93d3cud2luZGVsbi5kZS9jdXN0b21lci9hY2NvdW50L2luZGV4Lw,,/'
WINDELN_CART_URL = 'https://www.windeln.de/checkout/cart/index/'
WINDELN_APTAMIL_URL = 'http://www.windeln.de/aptamil-milchnahrung.html?ids=11902I5887I5999'
OUT_OF_STOCK_KEYWORD = 'ist momentan nicht'
APTAMIL_L2_4S = '<span class="span-8 name" itemprop="itemOffered">3 (800 g), 4'
APTAMIL_L2_4S_PRICE = '<span class="raw-price">'
APTAMIL_L2_4S_NOTAVAIL = '<span class="product-note align-right right" id="notShippable">Zur Zeit nicht lieferbar</span>'
APTAMIL_L2_4S_AVAIL = '<input type="text" value="0" name="qty">'

APTAMIL_L3_4S = '<td class="desc">3 (800 g), 1'
APTAMIL_L3_4S_PRICE = '<span class="price">'
APTAMIL_L3_4S_AVAIL = 'itemprop="availability" content="'
APTAMIL_L3_4S_NONE = 'out_of_stock'

class WXWindelnAPI(object):

    def __init__(self, username, pwd):
        self._username = username
        self._pwd = pwd
        self._token = None
        self._requests_session = requests.session()
        self._login_succ = False
    
    def _login(self):
        self._requests_session.cookies.clear_session_cookies()

        self._requests_session.get(WINDELN_URL, verify = True)
        self._requests_session.get(WINDELN_LOGIN_REFERER, verify = True)

        header = {}
        
        header['Referer'] = WINDELN_LOGIN_REFERER
        header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header['Accept-Encoding'] = 'gzip,deflate,sdch'
        header['Accept-Language'] = 'zh-CN,zh;q=0.8'
        header['Cache-Control'] = 'max-age=0'
        header['Connection'] = 'keep-alive'
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'
        header['Host'] = 'www.windeln.de'
        header['Origin'] = 'https://www.windeln.de'

        p = {}
        p['login[username]'] = self._username
        p['login[password]'] = self._pwd
        body = urllib.urlencode(p)
        
        resp = self._requests_session.post(WINDELN_LOGIN_URL, verify = True, data = body, headers = header)
        print resp.url
        
        if resp.status_code == 200:
            if resp.url.find('login') < 0:
                tracelog.info('Windeln(%s) login succ!' % self._username)
                self._login_succ = True
                return True
        
        return False        

    def old_aptamil_stock(self, html, start):
        price = 'unknown'
        out_of_stock = True
        
        price_s = html.find(APTAMIL_L3_4S_PRICE, start)
        if price_s > start:
            price_s = price_s + len(APTAMIL_L3_4S_PRICE)
            price_e = price_s + 5
            price = html[price_s:price_e]
        
        avail_s = html.find(APTAMIL_L3_4S_AVAIL, price_s)
        if avail_s > price_e:
            avail_s = avail_s + len(APTAMIL_L3_4S_AVAIL)
            avail_e = html.find('"', avail_s)
            avail = html[avail_s:avail_e]
            if avail.find(APTAMIL_L3_4S_NONE) >= 0:
                out_of_stock = True
            else:
                out_of_stock = False
            
        tracelog.info('old web: price %s, %s' % (price, out_of_stock))
        return (price, out_of_stock)
    
    def new_aptamil_stock(self, html, start):
        price = 'unknown'
        out_of_stock = True
        
        price_s = html.find(APTAMIL_L2_4S_PRICE, start)
        if price_s > start:
            price_s = price_s + len(APTAMIL_L2_4S_PRICE)
            price_e = price_s + 5
            price = html[price_s:price_e]
        
        not_avail_s = html.find(APTAMIL_L2_4S_NOTAVAIL, price_s)
        avail_s = html.find(APTAMIL_L2_4S_AVAIL, price_s)
        if not_avail_s > avail_s:
            out_of_stock = False
        else:
            out_of_stock = True
        
        tracelog.info('new web: price %s, %s' % (price, out_of_stock))
        return (price, out_of_stock)
        
    
    def get_aptamil_stock(self):
        r = self._requests_session.get(WINDELN_APTAMIL_URL, verify = True)

        resp_html = r.text
        
        new = resp_html.find(APTAMIL_L2_4S)
        old = resp_html.find(APTAMIL_L3_4S)
        
        if new > 0:
            return self.new_aptamil_stock(resp_html, new)
        
        if old > 0:
            return self.old_aptamil_stock(resp_html, old)
        
        tracelog.info('windeln web get error')  

if __name__ == '__main__':
    wx_api = WXWindelnAPI('allenxu@gmail.com', 'Xuweinan812185')
    price, stock = wx_api.get_aptamil_stock()
    
    print 'price %s, out_of_stock %s' % (price, stock)
    
