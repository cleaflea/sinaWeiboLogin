__author__ = 'cutejumper'

import sys
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import rsa
import binascii

class weiboLogin:
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': '',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    def get_servertime(self, username):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None

    def get_pwd(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        passwd = rsa.encrypt(message, key)
        passwd = binascii.b2a_hex(passwd)
        return passwd

    def get_user(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

    def get_account(self, filename):
        f = file(filename)
        flag = 0
        for line in f:
            if flag == 0:
                username = line.strip()
                flag += 1
            else:
                pwd = line.strip()
        f.close()
        return username, pwd

    def login(self, filename):
        username, pwd = self.get_account(filename)

        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
        try:
            servertime, nonce, pubkey, rsakv = self.get_servertime(username)
            print servertime
            print nonce
            print pubkey
            print rsakv
        except:
            print 'get servertime error!'
            return
        weiboLogin.postdata['servertime'] = servertime
        weiboLogin.postdata['nonce'] = nonce
        weiboLogin.postdata['rsakv'] = rsakv
        weiboLogin.postdata['su'] = self.get_user(username)
        weiboLogin.postdata['sp'] = self.get_pwd(pwd, servertime, nonce, pubkey)
        weiboLogin.postdata = urllib.urlencode(weiboLogin.postdata)
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
        req = urllib2.Request(
            url = url,
            data = weiboLogin.postdata,
            headers = headers
        )
        result = urllib2.urlopen(req)
        text = result.read()
        print text
        p = re.compile('location\.replace\(\"(.*)\"\)')
        try:
            login_url = p.search(text).group(1)
            print 'login url' + login_url
            # response = urllib2.urlopen(login_url)
            # html = response.read()
            urllib2.urlopen(login_url)
            print "Login success!"
            # print html
            return 1
        except:
            print 'Login error!'
            return 0