import argparse
from os import listdir, rename
from os.path import isfile, isdir, join, exists
import re

parser = argparse.ArgumentParser(description='Rename folders as with increasing numbers.')
parser.add_argument(dest='name', help='Base name for renaming.', type=str)
parser.add_argument('-i', dest='index', help='Index to start with.', default=1, type=int)
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-d', dest='digits', help='Number of digits.', default=2, choices=[2,3], type=int)
parser.add_argument('-t', dest='test', help='Test mode (no actual renaming).', action='store_true')
args = parser.parse_args()

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

if __name__ == '__main__':
    path = args.path
    index = args.index
    digits = args.digits

    folders = sorted_aphanumeric([f for f in listdir(path) if isdir(join(path, f))])
    names = []
    for fold in folders:
        # New filename
        if digits == 2: name = args.name + " %02d" %index
        elif digits == 3: name = args.name + " %03d" %index
        index += 1
        print('Treating ' + fold + ' -> ' + name)
        # Check if new name exists
        if fold == name:
            print('Skipping file' + fold + ': already has requested name') ; continue
        if exists(join(path,name)):
            raise ValueError('Stop: '+join(path,name)+' already exists.')
        names += [name]
    print('No naming issues.')
    if not args.test:
        for fold,name in zip(folders,names):
            print('Renaming ' + fold + ' to ' + name)
            rename(join(path,fold),join(path,name))
