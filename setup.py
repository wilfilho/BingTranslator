from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="ms_translator",
	packages = ["ms_translator"],
	version = '0.2.4',
	description = "Micrososft Translator API V2 for Python",
	long_description = read("README.rst"),
	author = "Will Filho",
	author_email = "dookgulliver@willfilho.com",
	license = "LGPL",
	install_requires = ["requests"],
	keywords = "microsoft translator bing",
	url = "https://github.com/dookgulliver/ms_translator",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Utilities",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
		],
)
