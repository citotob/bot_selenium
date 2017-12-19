import re
import os
import time
from datetime import datetime
from random import randint

#########################################################################################################################
# BCA Module
#########################################################################################################################
def transactionLogBCA(data, username, yesterday):
    lines = []
    new_data = []
    data = data[1:]
    timenow = datetime.now().strftime("%H:%M:%S")
    #config_file = os.getcwd().replace('TARIK_BANK','BOT')
    config_file = os.getcwd()
    if len(data):
        filename = config_file + "/data/" + yesterday + "_TransactionBCA_" + username + ".txt"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
            new_data = data[len(lines):len(data)]
        else:
            new_data = data
        with open(filename, 'w') as f:
            for d in data:
                d = [yesterday] + [timenow] + d[1:]
                f.write(" ".join(d) + "\n")
    return new_data, timenow

def pendingTransactionBCA(data, fname, yesterday, timenow, username):
    #config_file = os.getcwd().replace('TARIK_BANK','BOT')
    config_file = os.getcwd()
    filename = config_file + "/data/" + yesterday + "_pendingTransactionBCA_" + username + ".txt"
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
                        d = [yesterday] + [timenow] + d[1:]
                        f.write("||".join(d)+'\n')
    except:
        return 0

