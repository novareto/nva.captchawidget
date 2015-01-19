# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import grok
from zope.component import getMultiAdapter
from zope.interface import Interface
from zeam.form.base.markers import NO_VALUE
from zeam.form.base.widgets import WidgetExtractor
from zeam.form.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)


class CaptchaSchemaField(SchemaField):
    pass


class CaptchaFieldWidget(SchemaFieldWidget):
    grok.adapts(CaptchaSchemaField, Interface, Interface)

    def __init__(self, component, form, request):
        super(CaptchaFieldWidget, self).__init__(component, form, request)
        self.captcha = getMultiAdapter((form.context, request), name='captcha')


class CaptchaWidgetExtractor(WidgetExtractor):
    grok.adapts(CaptchaSchemaField, Interface, Interface)

    def extract(self):
        value, errors = super(CaptchaWidgetExtractor, self).extract()
        if errors:
            return (None, errors)
        if value is not NO_VALUE:
            value = str(value)
            captcha = getMultiAdapter(
                (self.form.context, self.request), name='captcha')
            if not captcha.verify(value):
                return (None, _(u"Invalid captcha input."))
            return (value, None)
        return (value, None)


def register():
    registerSchemaField(CaptchaSchemaField, ICaptcha)
