Fretsboard
==========

[![Build Status](https://travis-ci.org/Linkid/fretsboard.svg?branch=master)](https://travis-ci.org/Linkid/fretsboard)
[![Coverage Status](https://coveralls.io/repos/github/Linkid/fretsboard/badge.svg?branch=master)](https://coveralls.io/github/Linkid/fretsboard?branch=master)
[![Documentation Status](https://readthedocs.org/projects/fretsboard/badge/?version=latest)](https://fretsboard.readthedocs.io/en/latest/?badge=latest)

Fretsboard is a web scoreboard for the rhythm game Frets On Fire.

Instance (new): https://fretsboard.herokuapp.com

Instance (old): http://fretsonfire.sourceforge.net/charts/

Get in touch (via matrix): [#fretsboard:matrix.org](https://riot.im/app/#/room/#fretsboard:matrix.org)


![Screenshot scoreboard](https://raw.githubusercontent.com/Linkid/fretsboard/master/docs/source/_static/screenhsot_scoreboard.png "Screenshot scoreboard")


Status
======

A small instance is available.

This project is **still** in development.


How to run
==========

On a virtualenv:

```bash
git clone git@github.com:Linkid/fretsboard.git
cd fretsboard
pip install -r requirements.txt
./manage.py makemigrations scoreboard
./manage.py migrate
./manage.py runserver
```


Origin
======

This application comes from the old [Frets On Fire Charts Server](https://sourceforge.net/projects/fretsonfire/files/fretsonfire-chartserver/).

Other scoreboard were developped, in PHP:
- fofchart (2008): https://sourceforge.net/projects/fofchart/
- fofcs (2008): https://sourceforge.net/projects/fofcs/
- fretsweb-php (2009): https://sourceforge.net/projects/fretsweb/

For more information, see the [Frets On Fire forum post](https://www.fretsonfire.org/forums/viewtopic.php?f=21&t=60687).
