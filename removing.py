#!/usr/bin/python3
import argparse
from os import listdir, rename, remove
from os.path import isfile, isdir, join, exists

parser = argparse.ArgumentParser(description='Remove all files with a given string in the name.')
parser.add_argument(dest='word', help='Word to remove.', type=str)
parser.add_argument('-R', dest='recursive', help='Recursively remove in all subfolders.', action='store_true')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-i', dest='prompt', help='Prompt before removing.', action='store_true')
args = parser.parse_args()

def prompt(mode, file):
    while(1):
        ans = input(mode+' '+file+'? (y/n) > ')
        if ans == 'y': return True
        elif ans == 'n': return False

def removage(path, word):
    files = listdir(path)
    for file in files:
        if isfile(join(path,file)):
            if word in file and (not args.prompt or (args.prompt and prompt('Delete',file))):
                print('Removing '+join(path,file))
                remove(join(path,file))

if __name__ == '__main__':
    removage(args.path, args.word)
    if args.recursive:
        for file in listdir(args.path):
            if isdir(file):
                removage(join(args.path,file),args.word)
