#!/bin/bash

cd ~/code/transit2012/calc/ || exit 1

python3 transittweets.py venusobs 'transit04' > 2004.csv && 
python3 calc.py 2004 2004.csv > ../site/calc/2004.json

python3 transittweets.py venusobs venusobs > transit12.csv && 
python3 calc.py 2012 transit12.csv > ../site/calc/2012.json

