#!/bin/bash

export FLASK_APP=server.py
rm nohup.last.out
mv nohup.out nohup.last.out
nohup python3 -m flask run --port 9876 --host 0.0.0.0 &
echo "Tweetcool server started in background. Read the nohup.out file to read the output!"
