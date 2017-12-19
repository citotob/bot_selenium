#!/usr/bin/python

import re
import os
from datetime import datetime

#########################################################################################################################
# BCA Module
#########################################################################################################################
def transactionLogBCA(data, username):
    lines = []
    new_data = []
    data = data[1:]
    today = datetime.now().strftime("%Y%m%d")
    timenow = datetime.now().strftime("%H:%M:%S")
    if len(data):
        filename = os.getcwd() + "/data/" + today + "_TransactionBCA_" + username + ".txt"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = [l for l in f.readlines() if len(l) > 10]
            new_data = data[len(lines):len(data)+10]
        else:
            new_data = data
        with open(filename, 'w') as f:
            for d in data:
                d = [today] + [timenow] + d[1:]
                f.write(" ".join(d) + "\n")
    return new_data, timenow

def processTransactionBCA(data, username):
    today = datetime.now().strftime("%Y%m%d")
    filename = os.getcwd() + "/data/" + today + "_processTransactionBCA_" + username + ".txt"
    try:
        lines = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
        with open(filename, 'a+') as f:
            for d in data:
                if " ".join(d)+'\n' not in lines:
                    f.write(" ".join(d)+'\n')
    except Exception as e:
        print e

def pendingTransactionBCA(data, fname, timenow, username):
    today = datetime.now().strftime("%Y%m%d")
    filename = os.getcwd() + "/data/" + today + "_pendingTransactionBCA_" + username + ".txt"
    lines = []
    try:
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                lines = f.readlines()
        else:
            return 0
        with open(filename, 'a+') as f:
            for d in data:
                if d:
                    if d[len(d)-2] == 'CR':
                        d = [today] + [timenow] + d[1:]
                        f.write("||".join(d)+'\n')
    except:
        return 0

def updatePendingTransactionBCA(data, filename):
    try:
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if data in lines[i]:
                    lines[i] = ''
        with open(filename, 'w') as f:
            for line in lines:
                if line != '':
                    f.write(line)
    except Exception as e:
        print e

def writeNotFoundBCA(data, filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            for d in data:
                if " ".join(d[:len(d)-1]) in lines[i]:
                    print "Found"
                    lines[i] = ''
    with open(filename, 'w') as f:
        for d in data:
            if d != '' and type(d) == list and d !='\n':
                f.write(" ".join(d) + '\n')
            else:
                f.write(d)

def notFoundTransactionLogBCA(data, delay, name, close=None):
    today = datetime.now().strftime("%Y%m%d")
    #filename = today + "_pendingTransactionBCA.txt"
    filename = os.getcwd() + "/data/" + today + "_notFoundTransactionBCA.txt"
    print(filename)
    status = False
    try:
        lines = []
        found = None
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write('')
                f.close()
        with open(filename, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip('\n')
            wait = re.search(r'WAIT-\d+', line)
            if wait and name in line:
                line = line[:line.index(wait.group())-1]
                wait = wait.group()[5:]
                print (wait, line, lines)
                print (data)
                if " ".join(data) in line:
                    found = 1
                    if int(wait) >= delay or close:
                        status = True
                        lines[i] = ''
                    else:
                        wait = int(wait) + 1
                        lines[i] = line + ' WAIT-' + str(wait)
                        print lines[i]
        if not found and not close:
            lines.append(data + ['WAIT-1'])

        writeNotFoundBCA(lines, filename)

    except Exception as e:
        print e

    return status

