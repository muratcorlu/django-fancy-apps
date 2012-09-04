# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

PACKAGE = "fancy"
NAME = "django-fancy-apps"
DESCRIPTION = "Django Fancy Apps"
AUTHOR = u'Murat Çorlu'
AUTHOR_EMAIL = "muratcorlu@gmail.com"
URL = "http://github.com/muratcorlu/django-fancy-apps"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    #long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django >= 1.4',
        'django-taggit >= 0.8',
        'django-mptt >= 0.5.2'
    ],
)

