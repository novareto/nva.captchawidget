# -*- coding: utf-8 -*-

import grokcore.component as grok
from .field import ICaptcha
from zope.i18nmessageid import MessageFactory
from zope.component import getMultiAdapter
from zope.interface import Interface
from zeam.form.base.markers import NO_VALUE
from zeam.form.base.widgets import WidgetExtractor
from zeam.form.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)


_ = MessageFactory('nva.captchawidget')


class CaptchaSchemaField(SchemaField):
    pass


class CaptchaFieldWidget(SchemaFieldWidget):
    grok.adapts(CaptchaSchemaField, Interface, Interface)

    def __init__(self, component, form, request):
        super(CaptchaFieldWidget, self).__init__(component, form, request)
        self.captcha = getMultiAdapter((form.context, request), name='captcha.png')


class CaptchaWidgetExtractor(WidgetExtractor):
    grok.adapts(CaptchaSchemaField, Interface, Interface)

    def extract(self):
        value, errors = super(CaptchaWidgetExtractor, self).extract()
        if errors:
            return (None, errors)
        if value is not NO_VALUE:
            value = str(value)
            captcha = getMultiAdapter(
                (self.form.context, self.request), name='captcha.png')
            if not captcha.verify(value):
                return (None, _(u"Invalid captcha input."))
            return (value, None)
        return (value, None)


def register():
    registerSchemaField(CaptchaSchemaField, ICaptcha)
