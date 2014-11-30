from setuptools import setup
import os

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    raise Exception("warning: pypandoc module not found, could not convert Markdown to RST")

setup(
    name="bing_translator",
	packages = ["bing_translator"],
	version = '0.1',
	description = "Micrososft Translator API V2 for Python",
	long_description = read_md("README.md"),
	author = "Will Filho",
	author_email = "dookgulliver@willfilho.com",
	license = "LGPL",
	install_requires = ["requests"],
	keywords = ["microsoft translator","bing"],
	url = "https://github.com/dookgulliver/bing_translator",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3"
		]
)
