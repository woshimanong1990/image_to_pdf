# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from setuptools import setup, find_packages

setup(
    name="image_to_pdf",
    version="0.0.1",
    keywords=("image to pdf", "multi image to pdf"),
    description="local transfer file",
    long_description="one or multi image to pdf",
    license="MIT Licence",

    url="https://github.com/woshimanong1990/image_to_pdf",
    author="ant",
    author_email="qinghelanzhu@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "Pillow",
        "PyQt5",
    ],

    scripts=[],
    entry_points={
        'console_scripts': [
            'image_to_pdf = image_to_pdf.main:main'
        ]
    }
)