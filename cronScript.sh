#!/usr/bin/bash

DATE=`date +"%Y%m%d %H:%M"`
cd $HOME/Repositories/CovidStats && $HOME/Repositories/CovidStats/getStats.py 
git add ./reports/*
git commit -m "Hourly Update - ${DATE}"
git push
