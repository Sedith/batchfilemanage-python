#!/usr/bin/python3
from PIL import Image
import argparse
from os import listdir, rename
from os.path import isfile, isdir, join, exists
import re

parser = argparse.ArgumentParser(description='Number images in directory (jpgs and pngs).')
parser.add_argument('-i', dest='index', help='Index to start with.', default=1, type=int)
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-d', dest='digits', help='Number of digits.', default=3, choices=[2,3], type=int)
parser.add_argument('-R', dest='recursive', help='Recursively number all subdirectories.', action='store_true')
parser.add_argument('-Ri', dest='keepindex', help='Recursively number all subdirectories without reseting index.', action='store_true')
parser.add_argument('-t', dest='test', help='Test mode (no actual renaming).', action='store_true')
args = parser.parse_args()

def prompt(message):
    while(1):
        ans = input(message)
        if ans == 'y': return True
        elif ans == 'n': return False

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def numerotage(path, index, digits):
    files = sorted_aphanumeric([f for f in listdir(path)
                                if isfile(join(path, f))
                                and (f.lower().endswith('.png')
                                     or (f.lower().endswith('.jpg'))
                                     or (f.lower().endswith('.jpeg'))
                                )])
    valid_files = []
    conflict_files = []
    names = []
    conflict = False
    for file in files:
        # File extension
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'): ext = '.jpg'
        elif file.lower().endswith('.png'): ext = '.png'
        else: print('Skipping file' + file + ': not jpg or png') ; continue
        # New filename
        im = Image.open(join(path,file))
        if im.size[0] > im.size[1]:
            if digits == 2:   name = "%02d-%02d" %(index,index+1) + ext
            elif digits == 3: name = "%03d-%03d" %(index,index+1) + ext
            index += 2
        else:
            if digits == 2:   name = "%02d" %index + ext
            elif digits == 3: name = "%03d" %index + ext
            index += 1
        print('Treating ' + file + ' -> ' + name)
        # Check if new name exists
        if file == name:
            print('Skipping file ' + file + ': already has requested name') ; continue
        if exists(join(path,name)) and (name not in valid_files):
            print('Conflict with ' + file + ' -> ' + name)
            conflict = True
            names += ['tmp'+name]
        else:
            names += [name]
        valid_files += [file]
    if conflict:
        if not prompt('Conflicts: confirm before renaming (y/n) > '): exit()
    else:
        print('No naming issues.')
    if not args.test:
        for file,name in zip(valid_files,names):
            print('Renaming ' + file + ' to ' + name)
            rename(join(path,file),join(path,name))
        for name in names:
            if name.startswith('tmp'):
                print('Renaming ' + name + ' to ' + name[3:])
                rename(join(path,name),join(path,name[3:]))
    return index

if __name__ == '__main__':
    if args.recursive or args.keepindex:
        dirs = sorted_aphanumeric([join(args.path,d) for d in listdir(args.path) if isdir(join(args.path, d))])
        index = args.index
        for dir in dirs:
            print('Directory ' + dir)
            if not args.keepindex: index = args.index
            index = numerotage(dir, index, args.digits)
    else:
        numerotage(args.path, args.index, args.digits)
