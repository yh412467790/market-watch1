#!/bin/bash

i# any future command that fails will exit the script
set -e

# Delete the old repo
rm -rf /home/ec2-user/market_watch

# clone the repo again
git clone git@gitlab.com:se580/market_watch.git

sudo docker stop symbol_check
sudo docker rmi symbol_check

cd /home/ec2-user/market_watch
sudo ./build.sh
sudo ./run.sh


