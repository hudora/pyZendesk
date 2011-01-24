# encoding: utf-8
"""
zendesk.py - Zendesk.com automation

Written by Yurii Zolotko in behalf of HUDORA.
Updated by Christian Klein
Copyright (c) 2010, 2011 HUDORA. All rights reserved.

Configuration via config.py or environment:
ZENDESK_DOMAIN
ZENDESK_REMOTE_AUTH_TOKEN
ZENDESK_CREDENTIALS
"""

import huTools.http
import time
import urlparse
import xml.etree.ElementTree as ET
from urllib import urlencode
from hashlib import md5


try:
    import config
    get_config = lambda key: getattr(config, key, None)
except ImportError:
    import os
    get_config = os.getenv


def create_user(name, email):
    """Create new user in Zendesk"""

    root = ET.Element('user')
    ET.SubElement(root, 'name').text = name
    ET.SubElement(root, 'email').text = email

    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    url = urlparse.urljoin('https://%s.zendesk.com' % get_config('ZENDESK_DOMAIN'), '/users.xml')
    
    status, headers, content = huTools.http.fetch(url, content=ET.tostring(root),
                                                  headers=headers,
                                                  credentials=get_config('ZENDESK_CREDENTIALS'))
    return headers.get('Location')


def get_signature(name, email, timestamp):
    """Create signature for a remote auth link"""

    tmp = ''.join((name, email, get_config('ZENDESK_REMOTE_AUTH_TOKEN'), timestamp))
    return md5(tmp).hexdigest()


def create_link(name, email, timestamp=None, return_to=None):
    """Create remote auth link"""

    if timestamp is None:
        timestamp = str(int(time.time()))

    signature = get_signature(name, email, timestamp)
    params = {'name': name, 'email': email, 'timestamp': timestamp, 'hash': signature}
    if return_to:
        params['return_to'] = return_to

    link = urlparse.urlunparse(('https',
                                '%s.zendesk.com' % get_config('ZENDESK_DOMAIN'),
                                '/access/remote/',
                                '',
                                urlencode(params),
                                ''))
    return link


