import sys
import argparse
from collections import namedtuple

## Getting information from stdin (argv) ##
parser = argparse.ArgumentParser(description='Getting information to continue')
# Filename
parser.add_argument('filename', type=str,
                    help='A required filename')

# Columns
parser.add_argument('--columns', type=str, nargs='?',
                    help='A required columns to filter columns')

# Filter
parser.add_argument('--filter', type=str,
                    help='A required condition for filter')

# Format
parser.add_argument('--format', type=str,
                    help='A required format')
# Seperator
parser.add_argument('--seperator', type=str,
                    help='A required seperator')
args = parser.parse_args()
filename = args.filename
columns = args.columns
filter = args.filter
format = args.format
seperator = args.seperator
## End of getting information from user ##



# Define of namedtuples as Data Structures for the excercise
Master = namedtuple('Master', ['TYPE', 'N', 'DATETIME', 'ERRORLEVEL', 'DEVICEID', 'USERNAME', 'MESSAGE', 'MOBILEID'])
Slave = namedtuple('Slave', ['TYPE', 'N', 'DATETIME', 'ERRORLEVEL', 'DEVICEID', 'ACTION', 'MESSAGE', 'IP'])
# Define of maximum number of columns 
n_cols = 8

# A check for myself if I ran the program by debugging
# filename = input('Please Enter your CSV path: ')

### FILE LOADING AREA ###
try:
    # File opening
    fin = open(filename, 'r')
    print('File has succesfully loaded!')

except IOError:
    # In case could not open file
    print('Could not open ' + filename + ', closing now.')
    exit(1)

except NameError:
    # In case didn't initilize filename in argv
    print('You didnt enter file name, closing now.')
    exit(1)

### END OF FILE LOADING AREA ###

# Reading lines from file into an array
lines = fin.readlines()

# Define of 2 lists , 1 for master and 1 for slave
master_list = []
slave_list = []

for line in lines:
    # Splits each line into n_cols -1 commas
    values = [value.strip() for value in line.split(',', n_cols - 1)]
    # A check if its 'Master' line or 'Slave' line
    if line[0] == 'M':
        while len(values) < n_cols:
            values.append(None)
        master_list.append(Master(*values))
    else:
        while len(values) < n_cols:
            values.append(None)
        slave_list.append(Slave(*values))


#column_name = columns  # or use input('Please enter columns name you want to see, i.e. MobileID/Message: ')
column_name = [value.strip() for value in columns.split(',', columns.count(','))]

# Prints out of Master truple   
print('M: TYPE | N | DATETIME | ERRORLEVEL | DEVICEID | USERNAME | MESSAGE | MOBILEID ')
for i in range(len(master_list)):
    print(str(i+1) + '. ',end = '')
    for l in range(len(column_name)):
        try:
            print(str(column_name[l]).upper() + ' = ' + str(master_list[i].__getattribute__(column_name[l].upper())), end =' ')
        except AttributeError:
            print('Your entered column does not exist, please enter a correct column i.e. `DeviceID` / `Message`.')
            break
    print('')
# Prints out of Slave truple        
print('S: TYPE | N | DATETIME | ERRORLEVEL | DEVICEID | ACTION | MESSAGE | IP')
for k in range(len(slave_list)):
    print(str(k+1) + '. ', end='')
    for l in range(len(column_name)):
        print(str(column_name[l]).upper() + ' = ' +str(slave_list[k].__getattribute__(column_name[l].upper())), end =' ')
    print('')
    # print(column_name + ' = ' + master_list[4].__getattribute__(column_name.upper())) # by column name if name no known in advance


# TO DO LIST
# 1. Filter by condition
# 2. Formate choose option
# 3. Seperator choose option (i.e. space, comma)