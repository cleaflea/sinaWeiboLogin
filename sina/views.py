# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
import os
import weiboLogin
import urllib2

def rsaLogin(request):
    filesPath = os.path.join(os.path.dirname(__file__), '..', 'files').replace('\\','/')
    filePath = str(filesPath) + '/account.txt'

    WBlogin = weiboLogin.weiboLogin()
    resultList = WBlogin.login(filePath)
    if resultList == 1:
        print 'login successful'
        return HttpResponseRedirect('/weiboindex/')
    else:
        print 'login error!'
        return HttpResponse('ERROR')
    return HttpResponse('SUCCESSFUL')

def sinaindex(request):
    # proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)

    url = 'http://weibo.sina.com'

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    response = urllib2.urlopen(request)
    the_page = response.read()

    return HttpResponse(the_page)


