#!/usr/bin/env python

import os

from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), "README.md"), 'rb') as readme_file:
    readme = readme_file.read().decode('utf-8')

version = "1.6-dev"

setup(
    name="fretsboard",
    version=version,
    author="François Magimel",
    author_email="francois.magimel@perdu.fr",
    description="Fretsboard is a web scoreboard for the rhythm game Frets On Fire and similar",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="GPL License",
    url="https://github.com/Linkid/fretsboard",
    packages=['fretsboard', 'scoreboard'],
    platforms='any',
    zip_safe=True,
    python_requires=">=3.6",
    install_requires=[
        "django >= 3.1",
        "django-bootstrap3 >= 9.0",
        "cerealizer == 0.8.3",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
        "Topic :: Internet",
        "Topic :: Multimedia",
    ],
    keywords="scoreboard fofix fretsonfire",
)
