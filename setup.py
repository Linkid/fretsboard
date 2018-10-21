#!/usr/bin/env python

from setuptools import setup


version = "1.1"

setup(
    name="fretsboard",
    version=version,
    author="François Magimel",
    author_email="francois.magimel@perdu.fr",
    description="Fretsboard is a web scoreboard for the rhythm game Frets On Fire and similar",
    long_description=open("README.md", 'rb').read().decode('utf-8'),
    license="GPL License",
    url="https://github.com/Linkid/fretsboard",
    packages=['fretsboard', 'scoreboard'],
    platforms='any',
    zip_safe=True,
    install_requires=[
        "django >= 2.1",
        "django-bootstrap3 >= 9.0",
        "cerealizer == 0.8.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
        "Topic :: Internet",
        "Topic :: Multimedia",
    ],
    keywords="scoreboard fofix fretsonfire",
)
