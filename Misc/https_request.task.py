#!/usr/bin/python

import urllib2
import traceback
import ssl

from valarie.controller.messaging import add_message

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            headers = {
                'Connection' : 'keep-alive',
                'Cache-Control' : 'max-age=0',
                'Upgrade-Insecure-Requests' : 1,
                'User-Agent' : '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'Cookie: beaker.session.id=357eb371fae63cd6d5f00f805ad70969; __utma=22379560.922144949.1545506020.1545506020.1545506020.1; __utmc=22379560; __utmz=22379560.1545506020.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=22379560.|4=Customer=NO=1^31=Platform=N%2FA=1; _fbp=fb.1.1545506020771.2094238571; returnUrl=; __utmb=22379560.10.9.1545506470535; utag_main=v_id:0167d7565b3d001a3b9c121054d703078002e07000838$_sn:1$_ss:0$_pn:5%3Bexp-session$_st:1545508270542$ses_id:1545506020157%3Bexp-session'''
            }
            
            req = urllib2.Request(url = "https://battlelog.battlefield.com/bf4/servers", \
                                  headers = headers)
            
            f = urllib2.urlopen(url = req, \
                                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
            r = f.read()
            
            f.close()
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_FAILURE
            self.output.append(traceback.format_exc())
        
        return self.status