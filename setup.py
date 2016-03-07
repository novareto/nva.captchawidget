# -*- coding: utf-8 -*-
# Copyright (c) 2008-2013 Infrae. All rights reserved.
# See also LICENSE.txt

from setuptools import setup, find_packages
import os

version = '1.1.dev0'

tests_require = [
    ]


setup(name='nva.captchawidget',
      version=version,
      description="Captcha Widget for UVCSite",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        ],
      keywords='captcha',
      author='Christian Klinger',
      author_email='ck@novareto.de',
      url='',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['nva'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'skimpyGimpy',
        'zeam.form.base',
        'zeam.form.ztk',
        'zope.i18n',
        'zope.component',
        'zope.interface',
        'zope.schema',
        'zope.traversing',
        ],
      entry_points="""
      # -*- Entry points: -*-
      [zeam.form.components]
      captcha = nva.captchawidget.widget:register
      """,
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
