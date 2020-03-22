#/bin/bash
git pull
python3 generate.py
python3 generate2.py
touch lastupdate.txt
