#!/bin/bash
if ps -ef | grep -v grep | grep mtgapp.py ; then
        exit 0
else
	cd /home/jacob/Discord/mtgdiscordbot/
	source ./mtgbot/bin/activate
	python3 -m pip install -r requirements.txt
        python3 ./src/mtgbot.py
fi
