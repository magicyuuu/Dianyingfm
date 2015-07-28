# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import sys
sys.path.append('./src')
setup(
      name="dianyingfm",
      version="0.1",
      description="More powerful recursive dir. Support HTML pretty view in tree structure.",
      long_description="",
      author="magicyuuu",
      author_email="magicyu1986@gmail.com",
      url="http://www.github.com/magicyuuu/dianyingfm",
      license="MIT",
      packages=["src/com/magicyu/dianyingfm"],
      include_package_data=True,
      package_data={"dianyingfm": ["*.py"]},
      install_requires=['pyquery'],
      keywords=["dir", "doc", "pydoc", "html"],
)

