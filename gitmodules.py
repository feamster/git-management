#!/usr/bin/env python3

import os
import sys
import subprocess
import re

def gitmodules(path, regexp=r'old'):

    print('gitmodules: ' + path + '.gitmodules')

    # read each line of .gitmodules
    with open(path + '.gitmodules', 'r') as f:
        lines = f.readlines()
        # read three lines at a time
        for i in range(0, len(lines), 3):
            # get the path
            path = re.search(r'path = (.*)', lines[i+1]).group(1)
            # get the url
            url = re.search(r'url = (.*)', lines[i+2]).group(1)
            # next if url matches regexp
            if re.search(regexp, path):
                continue
            for j in range(0, 3):
                print(lines[i+j], end='')

            # clone the repo
            #subprocess.run(['git', 'clone', url, path], cwd=path)





def main():
    # get path as command line argument
    path = sys.argv[1]
    gitmodules(path)

if __name__ == '__main__':
    main()
