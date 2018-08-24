#!/usr/bin/env bash
source ./utils.sh

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable

make
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/

cd ../
rm -r redis-stable
rm redis-stable.tar.gz