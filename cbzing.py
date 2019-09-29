import argparse
from os import listdir, rename, remove, getcwd
from os.path import isfile, isdir, join
from shutil import make_archive, move
import re
parser = argparse.ArgumentParser(description='Zip all folders in working directory and rename them to .cbz.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-d', dest='delete', help='Delete folders after zipping.', action='store_true')
parser.add_argument('-t', dest='target', help='Destination folder of zipped files.', default=None, type=str)
parser.add_argument('-i', dest='prompt', help='Prompt before every zipping and removal.', action='store_true')
args = parser.parse_args()

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def prompt(mode, file):
    while(1):
        ans = input(mode+' '+file+'? (y/n) > ')
        if ans == 'y': return True
        elif ans == 'n': return False

if __name__ == '__main__':
    path = args.path
    if args.target is None: target = path
    else: target = args.target

    dirs = sorted_aphanumeric([d for d in listdir(path) if isdir(join(path, d))])
    for file in dirs:
        if (args.prompt and prompt('Zipping',file)) or not args.prompt:
            file_name=make_archive(file, 'zip', join(getcwd(),path), file)
            move(file+'.zip', join(target,file+'.cbz'))
            if args.delete and ((args.prompt and prompt('Delete',file)) or not args.prompt):
                remove(join(path,file))
