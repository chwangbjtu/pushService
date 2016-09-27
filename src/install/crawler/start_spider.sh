#!/bin/bash
project=$1
spider=$2

#http://localhost:6800/schedule.json -d project=youku_recent -d spider=youku_cat_newest
curl http://localhost:6800/schedule.json -d project=$project -d spider=$spider
