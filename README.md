# Analyzer
A program which filters log files into whatever stdin wants
### An example of command line lunch command:
`python main.py 11.csv --columns type,n,datetime,message,mobileid,ip --filter datetime>20 --format value2 --seperator ';'`

# 25/08/2019
- Uploaded file
- To start the program use in the command line : python main.py (log's filename) --columns (columns filter) --filter (filter) --format (format) --seperator

# TODO List:
1. filter by condition function
