#!/usr/bin/env python
# -*- coding: utf-8 -


import cStringIO
import logging
import pycurl


class SSLClient(object):
    """
    Curl client for SSL certificates & CA bundles.
    """

    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        self.log = logging.getLogger(__name__)
        self.log.debug('SSLClient init host:%s, port:%d' % (host, port))

    def set_cert(self, key_file=None, ca_info=None, passwd_cb=None):
        self.key_file = key_file
        self.ca_info = ca_info
        self.ssl_pass = passwd_cb
        self.log.debug('Certificate set pem:%s, ca:%s, password callback:%s' % (
            key_file, ca_info, passwd_cb))

    def set_user(self, httpuser, httppwd):
        """
        Sets the curl --user option httpuser:httppwd
        """
        self.log.debug('setting user:pass as %s:%s' % (httpuser, httppwd))
        self.user = httpuser
        self.pwd = httppwd

    def request(self, method, url, postdata=None, timeout=None):
        """
        Does a curl post request, optional timeout.

        No exception handling whatsoever, the reason being that SSL
        can be somewhat fickle and therefore the code using this client
        should handle those intricacies
        """

        if not url.startswith('http'):
            url = 'https://%s:%s%s' % (self.host, self.port, url)
        self.log.debug(url)

        buffer = cStringIO.StringIO()
        curl = pycurl.Curl()

        def _debug(debug_type, debug_msg):
            self.log.debug("debug(%d): %s" % (debug_type, debug_msg))

        curl.setopt(pycurl.VERBOSE, 0)
        curl.setopt(pycurl.DEBUGFUNCTION, _debug)

        if method == 'POST' and postdata:
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDS, postdata)

        if timeout:
            curl.setopt(pycurl.TIMEOUT_MS, timeout)

        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.setopt(pycurl.NOSIGNAL, 1)

        curl.setopt(pycurl.SSLVERSION, 3)
        self.log.debug('certfile: %s' % self.key_file)
        curl.setopt(pycurl.SSLCERT, self.key_file)

        curl.setopt(pycurl.SSLCERTPASSWD, self.ssl_pass)

        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)

        if self.ca_info:
            self.log.debug('CAINFO: %s' % self.ca_info)
            curl.setopt(pycurl.CAINFO, self.ca_info)

        curl.setopt(pycurl.USERPWD,
            '%s:%s' % (self.user, self.pwd))

        self.log.debug('curl.USERPWD: %s:%s' % (self.user, self.pwd))

        curl.perform()
        buffer.seek(0)
        r = buffer.getvalue()
        buffer.close()
        return r
