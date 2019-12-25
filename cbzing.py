#!/usr/bin/python3
import argparse
from os import listdir, rename, getcwd
from os.path import isfile, isdir, join, exists
from shutil import make_archive, move, rmtree
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

def remove_folder(path):
    # check if folder exists
    if exists(path):
         rmtree(path)
    else:
         print('Folder does not exist.')

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
        if not args.prompt or (args.prompt and prompt('Zipping',file)):
            print('Treating '+file)
            if exists(join(path,file,'.zip')):
                print('Skipping: zip file already exists in working directory')
                continue
            if exists(join(target,file,'.cbz')):
                print('Skipping: cbz file already exists in target directory')
                continue
            make_archive(file, 'zip', join(getcwd(),path), file)
            move(file+'.zip', join(target,file+'.cbz'))
            if args.delete and (not args.prompt or (args.prompt and prompt('Delete',file))):
                remove_folder(join(path,file))
