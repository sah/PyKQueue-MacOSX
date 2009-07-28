# -*- coding: utf-8 -*-
# setup.py
from distutils.core import setup, Extension

setup(
    name="kqsyscall",
    version="1.3",
    ext_modules=[
        Extension("kqsyscall", sources=["kqsyscallmodule.c"])
    ]
)
