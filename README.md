# Analyzer
### Requirements:

![requirements-python](https://img.shields.io/badge/requirements-python--3.6-brightgreen.svg)

### General:
A program which filters log files into whatever stdin wants

### An example of command line lunch command:
`python main.py 11.csv --columns type,n,datetime,message,mobileid,ip --filter datetime>20 --format table`

### General Information:
#### About the CSV:
The CSV in general contains 2 types of lines, Master and Slave.
There are some rows with more available values than the others, and in these cases, the program will auto fill N/A for these blank spaces.
- Columns for Master lines:
`TYPE, N, DATETIME, ERRORLEVEL, DEVICEID, USERNAME, MESSAGE, MOBILEID`
- Columns for Slave lines:
`TYPE, N, DATETIME, MESSAGE, MOBILEID, IP ` 


### Argv & Argc options:
#### Command Line:
Inside the program, you'll have to lunch it by the command-line by typing `python main.py <filename> --columns <column>,<column>,... --filter <filter condition here> --format <table/list>'`

Difference between formats:
1. --format table:
If you'll type --format table then the program will print the results in 2 tables, one for slave and other one for master.
e.g : `TYPE = S;N = 2;DATETIME = 14/08/2019 11:45;MESSAGE = DHCP worked;MOBILEID = None;IP = 10.0.0.1;`

2. --format list:
If you'll type --format list then the program will print 2 lists one for master and one for slave.
e.g : `S;2;14/08/2019 11:45;DHCP worked;None;10.0.0.1;`

### Input / Output examples:
1. - Input - `python main.py 11.csv --columns type,n,datetime,mobileid --filter n==1 --format table`
   - Output - 
   ![Image description](/img/output1.png)

2. - Input - `python main.py 11.csv --columns type,n,datetime,mobileid,deviceid --filter username==tal --format list`
   - Output - 
   ![Image description](/img/output2.png)



### Programmed with:
1. Python 3
