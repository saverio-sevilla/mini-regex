from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Regex engine'
LONG_DESCRIPTION = 'A simple regex engine for Python 3'

setup(
    name="mini-regex",
    version= "0.01",
    author="Saverio Sevilla",
    author_email="<saveriosevilla@gmail.com>",
    description= "Regex engine for Python3",
    long_description="A simple Regex engine for Python 3, supports captures",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'regex'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
    ]
)