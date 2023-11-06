"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='word2asciidoc',
    version='0.1.1',
    description='Fix generated asciidoc files for AAS specifications',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/admin-shell-io/word2asciidoc',
    author='Igor Garmaev',
    author_email='garmaev@gmx.net',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
    ],
    license="License :: OSI Approved :: MIT License",
    keywords='fix aas submodel asciidoc word python',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>=3.7',
    install_requires=['pillow', 'wand'],
    py_modules=['word2asciidoc'],
    entry_points={
        'console_scripts': [
            'fix_adoc = word2asciidoc.fix_adoc:main',
        ],
    })
