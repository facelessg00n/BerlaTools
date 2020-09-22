# BerlaTools

## Tools to simplify analysis of BERLA iVe data.
Work in progress.
Python tools to analyse data from Berla iVe extracts in CSV format.
#
1. ### **berlaJoin** - brings in device friendly name and details to contacts, SMS and call CSV's so you dont have to go by MAC addresses etc. Also normalises timestamps allowing easier analysis.

2. ### **berlaNetwork** - Work in progress. Utilises networkx and pandas to analyse connon numbers between paired devices and generate a visualisation.
![Sample](samples/sample.png)
#
## Dependencies
Built and tested on python 3.8 but other versions of 3 should be fine. 
#### Requires PANDAS and TQDM to be installed.

https://pandas.pydata.org

`pip3 install tqdm`

https://github.com/tqdm/tqdm

`pip3 install tqdm`

### berlaNetwork also requires networkX

https://networkx.github.io

`pip3 install networkx`


#
## Usage
Place the python file is the same direcotry as CSV files to be analysed.
Then run with run with `python3 berlaJoin.py`  or `python3 berlaNetwork.py`
Converted files will be output to the same directory.\
As always you must verify the results.