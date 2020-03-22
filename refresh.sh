#/bin/bash
cd COVID-19
git pull
cd ..
cd coronadata
git pull
cd ..
git pull
python3 generate.py
python3 generate2.py
touch lastupdate.txt
