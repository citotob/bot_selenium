import re
import os

with open(os.getcwd() + "/_settings1.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip('\n')
        search_nDelay = re.search(r'WAIT_DELAY\s*\=\s*\d+', line)
        if search_nDelay:
            nDelay = search_nDelay.group()
            print(nDelay)
            nDelay = nDelay[len(nDelay)-1].strip(' ')

print(nDelay)
