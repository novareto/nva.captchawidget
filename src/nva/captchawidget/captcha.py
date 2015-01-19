# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import os.path
import random
import hashlib
import sys
import time
import hmac

from skimpyGimpy import skimpyAPI

import grok
from zope.interface import Interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

# Restricted set to avoid 0/o/O or i/I/1 confusion
CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

COOKIE_ID = 'nva.captcha'
WORDLENGTH = 7
FONTPATH = os.path.join(os.path.dirname(__file__), 'tektite.bdf')
SECRET = "CHANGEME"

_TEST_TIME = None


def digest(secret, *args):
    assert len(args) > 1, u'Too few arguments'
    challenge = hmac.new(secret, str(args[0]), hashlib.sha1)
    for arg in args[1:]:
        challenge.update(str(arg))
    return challenge.hexdigest()


class RenderedCaptcha(object):

    def __init__(self, context, request, word):
        self.context = context
        self.request = request
        self.word = word

    def set_headers(self, type):
        response = self.request.response
        response.setHeader('content-type', type)
        # no caching please
        response.setHeader('cache-control', 'no-cache, no-store')
        response.setHeader('pragma', 'no-cache')
        response.setHeader('expires', 'now')

    def __call__(self):
        raise NotImplementedError


class ImageCaptcha(RenderedCaptcha):
    """Image version of the captcha.
    """

    def __call__(self):
        self.set_headers('image/png')
        return skimpyAPI.Png(self.word, speckle=0.5, fontpath=FONTPATH).data()


class Captcha(grok.View):
    grok.name('captcha.png')
    grok.context(Interface)
    grok.require('zope.Public')

    _session_id = None

    def _setcookie(self, value):
        """Set the session cookie
        """
        response = self.request.response
        if COOKIE_ID in response._cookies:
            # clear the cookie first, clearing out any expiration cookie
            # that may have been set during verification
            del response._cookies[COOKIE_ID]
        response.setCookie(COOKIE_ID, value, path='/')

    def _generate_session(self):
        """Create a new session id
        """
        if self._session_id is None:
            value = hashlib.sha1(str(random.randrange(sys.maxint))).hexdigest()
            self._session_id = value
            self._setcookie(value)

    def _verify_session(self):
        """Ensure session id and cookie exist
        """
        if not self.request.has_key(COOKIE_ID):
            if self._session_id is None:
                # This may happen e.g. when the user clicks the back button
                self._generate_session()
            else:
                # This may happen e.g. when the user does not accept the cookie
                self._setcookie(self._session_id)
            # Put the cookie value into the request for immediate consumption
            self.request.cookies[COOKIE_ID] = self._session_id

    def _generate_words(self):
        """Create words for the current session

        We generate one for the current 5 minutes, plus one for the previous
        5. This way captcha sessions have a livespan of 10 minutes at most.

        """
        session = self.request[COOKIE_ID]
        nowish = int((_TEST_TIME or time.time()) / 300)
        seeds = [
            digest(SECRET, session, nowish),
            digest(SECRET, session, nowish - 1)]

        words = []
        for seed in seeds:
            word = []
            for i in range(WORDLENGTH):
                index = ord(seed[i]) % len(CHARS)
                word.append(CHARS[index])
            words.append(''.join(word))
        return words

    def _url(self, filename):
        return '%s/%s' % (self.application_url(), filename)

    def image_tag(self):
        self._generate_session()
        return '<img src="%s" alt="captcha"/>' % (self._url('captcha.png'),)

    def render(self):
        self._verify_session()
        captcha = ImageCaptcha(
            self.context,
            self.request,
            self._generate_words()[0])
        return captcha()

    def verify(self, input):
        if not input:
            return False
        result = False
        try:
            for word in self._generate_words():
                result = result or input.upper() == word.upper()
            # Delete the session key, we are done with this captcha
            self.request.response.expireCookie(COOKIE_ID, path='/')
        except KeyError:
            pass  # No cookie

        return result
