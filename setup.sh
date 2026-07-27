#!/bin/sh

mkdir Data
touch Data/config.json
touch Data/users.json
touch Data/periodsData.json
echo '''{"TOKEN":"","OWNER_ID":""}''' > Data/config.json
echo "[]">Data/users.json
pythom -m pip install -r requirments.txt
