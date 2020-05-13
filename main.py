import re
import copy
from beautifultable import BeautifulTable
import argparse

# Command line inputs (argv)
parser = argparse.ArgumentParser(description='Necessary information to run the program.')
parser.add_argument('filename',
                    type=str,
                    help='A required filename to investigate, i.e: <filename>.txt')
parser.add_argument('--columns',
                    type=str,
                    nargs='?',
                    help='Columns to filter, i.e: --columns datetime,ip')
parser.add_argument('--filter',
                    type=str,
                    help='A condition for filter, i.e --filter errorlevel>20')
parser.add_argument('--format',
                    type=str,
                    help='Format to display, i.e: --format value')
parser.add_argument('--seperator',
                    type=str,
                    help='Choose the seperator you want to display, i.e: --seperator `;`')
args = parser.parse_args()

# LL's Nodes
class Node:
    def __init__(self, dataval = None):
        self.dataval = dataval,
        self.nextval = None

# Linked List's class
class LinkedList:
    def __init__(self):
        self.headval = None

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        lastElement = self.headval
        while(lastElement.nextval):
            lastElement = lastElement.nextval
        lastElement.nextval = NewNode

    def printList(self):
        printVal = self.headval
        while printVal is not None:
            print(printVal.dataval)
            printVal = printVal.nextval

class Analyzer:
    def __init__(self, columns, filter, format, filename):
        self.filename = filename
        self.columns = columns
        self.filter = re.split(',', filter)
        self.format = format
        self.masterCols = ['TYPE', 'N', 'DATETIME', 'ERRORLEVEL', 'DEVICEID', 'USERNAME', 'MESSAGE', 'MOBILEID']
        self.slaveCols = ['TYPE', 'N', 'DATETIME', 'ERRORLEVEL', 'DEVICEID', 'ACTION', 'MESSAGE', 'IP']
        self.masterLL = None
        self.slaveLL = None
        self.file = None
        self.fileLines = None
        self.upperCols()

    def upperCols(self):
        upperCols = []
        cols = ''.join(self.columns)
        cols = cols.split(",")
        for col in cols:
            upperCols.append(col.upper())
        self.columns = upperCols


    def getFile(self):
        try:
            self.file = open(self.filename, 'r')
            print(self.filename + ' has successfully loaded')
            print("-" * len(self.filename) + "-" * 24)
        except Exception:
            print('Couldn\'t open ' + self.filename + ', Please try again.')

    def getMasterLines(self):
        self.masterLL = LinkedList()
        if self.fileLines == None:
            self.fileLines = self.file.readlines()

        for line in self.fileLines:
            if line[0] == 'M':
                # Splitting each master line with commas
                values = [value.strip() for value in line.split(',', len(self.masterCols) - 1)]
                finalLine = []
                # Checks line with each of the filters inserted by user
                if self.filter is not None or len(self.filter) > 0:
                    for eaFilter in self.filter:
                        finalLine = self.convertFilterToCondition(eaFilter, values, self.masterCols)
                        if finalLine is None:
                            break
                if finalLine is not None:
                    # Filtering by columns inserted by user
                    finalLine = self.saveNesscaryParts(values, self.masterCols);
                    # Adding to master's linked list.
                    self.masterLL.AtEnd(finalLine)
        # Prints the linked list by inserted format
        if self.masterLL.headval == None:
            print('\nThere\'re no master lines using your filter.')
        elif ''.join(self.format).upper() == "TABLE":
            self.convertToTable(self.masterCols, self.masterLL)
        elif ''.join(self.format).upper() == "LIST":
            print('Printing master list:')
            self.convertToList(self.masterCols, self.masterLL)
        else:
            print("Nothing to print, format is not correct, please choose one of 'LIST' / 'TABLE' formats")

    def getSlaveLines(self):
        self.slaveLL = LinkedList()
        if self.fileLines == None:
            self.fileLines = self.file.readlines()

        for line in self.fileLines:
            if line[0] == 'S':
                # Splitting each master line with commas
                values = [value.strip() for value in line.split(',', len(self.slaveCols) - 1)]
                finalLine = []
                # Checks line with each of the filters inserted by user
                if self.filter is not None or len(self.filter) > 0:
                    for eaFilter in self.filter:
                        finalLine = self.convertFilterToCondition(eaFilter, values, self.slaveCols)
                        if finalLine is None:
                            break
                if finalLine is not None:
                    # Filtering by columns inserted by user
                    finalLine = self.saveNesscaryParts(values, self.slaveCols)
                    self.slaveLL.AtEnd(finalLine)
        # Prints the linked list by inserted format
        if self.slaveLL.headval == None:
            print('\nThere\'re no slave lines using your filter.')
        elif ''.join(self.format).upper() == 'TABLE':
            self.convertToTable(self.slaveCols, self.slaveLL)
        elif ''.join(self.format).upper() == 'LIST':
            print('Printing slave list:')
            self.convertToList(self.slaveCols, self.slaveLL)
        else:
            print("Nothing to print, format is not correct, please choose one of 'LIST' / 'TABLE' formats")

    def saveNesscaryParts(self, line, cols):
        colIndexes = []
        # Getting cols indexes
        for idx,col in enumerate(cols):
            for column in self.columns:
                if col == column:
                    colIndexes.append(idx)

        # Getting columns to delete
        colsToDelete = []
        for idx, col in enumerate(cols):
            if idx not in colIndexes:
                colsToDelete.append(idx)

        # Deleting unnecessary parts from inserted line
        for index in reversed(colsToDelete):
            if len(line) > index:
                del line[index]

        return line

    def convertFilterToCondition(self, filter, line, mainCols):
        operator = ""
        if ">=" in filter:
            operator = ">="
        elif ">" in filter:
            operator = ">"
        elif "<=" in filter:
            operator = "<="
        elif "<" in filter:
            operator = "<"
        elif "==" in filter:
            operator = "=="
        elif "!=" in filter:
            operator = "!="
        if operator == ">" or operator == ">=" or operator == "<" or operator == "<=":
            newFilter = re.split(operator, filter)
            upperCol = newFilter[0].upper()
            for idx,col in enumerate(mainCols):
                if upperCol == col:
                    if(eval(line[idx] + operator + newFilter[1])):
                        return line
                    else:
                        return None
        elif operator == "!=":
            newFilter = re.split(operator, filter)
            upperCol = newFilter[0].upper()
            for idx, col in enumerate(mainCols):
                if upperCol == col:
                    if (line[idx] != newFilter[1]):
                        return line
                    else:
                        return None
        else:
            newFilter = re.split(operator, filter)
            upperCol = newFilter[0].upper()
            for idx, col in enumerate(mainCols):
                if upperCol == col:
                    if(len(line) - 1 < idx):
                        return None
                    elif (line[idx] == newFilter[1]):
                        return line
                    else:
                        return None

    def convertToTable(self, cols, list):
        relatedCols=[]
        # Ordering cols by masterCols / slaveCols
        for idx, col in enumerate(cols):
            for column in self.columns:
                if col == column:
                    relatedCols.append(col)

        table = BeautifulTable()
        table.column_headers = relatedCols
        listElem = list.headval
        # Looping through the related linked list and adding it to table
        while(listElem is not None):
            row = listElem.dataval[0]
            while(len(row) < len(relatedCols)):
                row.append('N/A')
            table.append_row(row)
            listElem = listElem.nextval
        print(table)

    def convertToList(self, cols, list):
        columns = copy.deepcopy(cols);
        # Getting only the necessary cols by order of slaveCols / masterCols
        for col in columns:
            if col not in self.columns:
                columns.remove(col)
        loopingList = list.headval;

        # Looping through the related linked list and printing it
        i = 1
        while(loopingList is not None):
            print(str(i), end=". ")
            for idx,col in enumerate(columns):
                if idx == len(loopingList.dataval[0]) - 1:
                    print(col + "= " + loopingList.dataval[0][idx])
                elif idx < len(loopingList.dataval[0]) - 1:
                    print(col + "= " + loopingList.dataval[0][idx] + ", ", end="")
            i = i + 1
            loopingList = loopingList.nextval



if __name__ == '__main__':
    analyzer = Analyzer(args.columns, args.filter, args.format, args.filename)
    analyzer.getFile()
    analyzer.getMasterLines()
    analyzer.getSlaveLines()

