# encoding: utf-8
"""
zendesk.py - Zendesk.com automation

Written by Yurii Zolotko in behalf of HUDORA.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import os
import urllib2
from urllib import basejoin, urlencode
from time import time
from hashlib import md5

__all__ = ('create_user', 'sign_link', 'create_link')

DEBUG_LEVEL = 1

def create_user(name, email):
    """Create new user in Zendesk"""
    
    url = basejoin('https://%s.zendesk.com' % os.getenv('ZENDESK_DOMAIN', ''), 'users.xml')
    auth_handler = urllib2.HTTPBasicAuthHandler()
    username, password = os.getenv('ZENDESK_CREDENTIALS', ':').split(':', 2)
    auth_handler.add_password(realm='Web Password', uri=url, user=username, passwd=password)

    class SetXmlContentType(urllib2.BaseHandler):
        def http_request(self, req):
            req.add_header('Content-Type', 'application/xml; charset=utf-8')
            return req

    opener = urllib2.build_opener(SetXmlContentType(), auth_handler,
        urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL))
    data = '<user><name>%s</name><email>%s</email></user>' % (name, email)
    response = opener.open(url, data=data)
    return response.info().getheader('Location')


def sign_link(name, email, timestamp):
    """Sign remote auth link"""
    token = name + email + os.environ.get('ZENDESK_REMOTE_AUTH_TOKEN', '') + str(timestamp)
    return basejoin('https://%s.zendesk.com' % os.getenv('ZENDESK_DOMAIN'), '/access/remote/?' + urlencode({
        'name': name,
        'email': email,
        'timestamp': timestamp,
        'hash': md5(token).digest().encode('hex')}))


def create_link(name, email):
    """Create remote auth link"""
    return sign_link(name, email, int(time()))


if __name__ == '__main__':
    from sys import argv
    if argv[1] == 'createuser':
        print create_user(argv[2], argv[3])
    elif argv[1] == 'createlnk':
        print create_link(argv[2], argv[3])
    elif argv[1] == 'signlnk':
        print sign_link(argv[2], argv[3], argv[4])
