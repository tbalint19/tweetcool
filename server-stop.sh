#!/bin/bash

pid="$(pgrep -f 9876)"
if [ ${#pid} -ge 1 ]; then 
  kill ${pid}
  echo "Tweetcool killed"
else
  echo "Tweetcool is not running"
fi
