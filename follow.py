import os

def follow(filename):
    with open(filename, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line == '':
                continue
            yield line
