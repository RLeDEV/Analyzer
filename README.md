# Analyzer
### Requirements:

![requirements-python](https://img.shields.io/badge/requirements-python--3.6-brightgreen.svg)

### General:
A program which filters log files into whatever stdin wants

### An example of command line lunch command:
`python main.py 11.csv --columns type,n,datetime,message,mobileid,ip --filter datetime>20 --format value2 --seperator ';'`

### General Information:
#### About the CSV:
The CSV in general contains 4 types of tabels which are stored in the code by tuples.
Once the program prints one of the types it will print before it the columns of the specific type, so you can understand the meaning of each colum printed by the program.

For example: 
If the system will print `S: TYPE | N | DATETIME | MESSAGE | MOBILEID | IP |` 
and then
`S;1;14/08/2019 11:41;User tal logged in;None;None;`
Then you'll be able to figure out that you're looking at 'S' table.

### Argv & Argc options:
#### Command Line:
Inside the program, you'll have to lunch it by the command-line by typing `python main.py <filename> --columns <column>,<column>,... --filter <filter condition here> --format <value/value2> --seperator '<seperator>'`

Difference between formats:
1. --format value:
If you'll type value then the program will print each column's name and its value.
e.g : `TYPE = S;N = 2;DATETIME = 14/08/2019 11:45;MESSAGE = DHCP worked;MOBILEID = None;IP = 10.0.0.1;`

2. --format value2:
If you'll type value2 then the program will print only the column's value without its name.
e.g : `S;2;14/08/2019 11:45;DHCP worked;None;10.0.0.1;`

### Programmed with:
1. Python 3
