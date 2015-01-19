# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.schema import ASCIILine
from zope.schema.interfaces import IASCIILine


class ICaptcha(IASCIILine):
    """A field for captcha validation
    """


@implementer(ICaptcha)
class Captcha(ASCIILine):
    pass
