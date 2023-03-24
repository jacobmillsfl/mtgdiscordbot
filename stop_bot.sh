#!/bin/bash

ps -ef | grep mtg | grep -v "grep" | cut -d" " -f6 | while read pid; do kill -9 "$pid"; done
