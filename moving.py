#!/usr/bin/python3
import argparse
from os import listdir, rename
from os.path import isfile, isdir, join, exists

parser = argparse.ArgumentParser(description='Move all files contain in subfolders in working directory.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-i', dest='prompt', help='Prompt before moving.', action='store_true')
parser.add_argument('-c', dest='here', help='Move all files from working directory to its parent (forced prompt).', action='store_true')
args = parser.parse_args()

def prompt(mode, file):
    while(1):
        ans = input(mode+' '+file+'? (y/n) > ')
        if ans == 'y': return True
        elif ans == 'n': return False

def moving(dir, target, _prompt):
    subfolders = []
    for file in listdir(dir):
        if file.startswith('.'): continue
        if isdir(join(dir,file)):
            subfolders += [join(dir,file)]
        else:
            if not _prompt or (_prompt and prompt('Move',join(dir,file))):
                print('Moving '+join(dir,file)+' to '+join(target,file))
                if exists(join(target,file)):
                    print('Skipping: '+join(target,file)+' already exists.')
                else:
                    rename(join(dir,file),join(target,file))
    return subfolders

if __name__ == '__main__':
    path = args.path
    if args.here:
        moving(path,join(path,'..'), True)
    else:
        folders = []
        for dir in listdir(path):
            if isdir(join(path,dir)) and not dir.startswith('.'): folders += [join(path,dir)]
        while folders != []:
            folder = folders.pop()
            folders += moving(folder, path, args.prompt)
