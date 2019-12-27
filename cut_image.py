#!/usr/bin/python3
import cv2
import argparse
from os import listdir, rename
from os.path import isfile, isdir, join, exists
import re

parser = argparse.ArgumentParser(description='Cut images in half.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-i', dest='interactive', help='Display and prompt for each image.', action='store_true')
parser.add_argument('-n', dest='ignore', help='Filenames of images to ignore.', default=[]  , type=str, nargs='*')
parser.add_argument('-o', dest='offset', help='Offset in pixels (positive to the right).', default=0, type=int)
args = parser.parse_args()

def prompt(file):
    while(1):
        ans = input(file+' - ok ? (y/n/(i)gnore/offset) > ')
        if ans == 'y': return True
        elif ans == 'n': return False
        elif ans == 'i': return 'ignore'
        try:
            read = int(read)
        except:
            continue
        return read

def cut(img, offset):
    half = round(img.shape[1]/2) + args.offset
    left = img[:,0:half]
    right = img[:,half+1:-1]
    return (left, right)

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

if __name__ == '__main__':
    path = args.path
    files = sorted_aphanumeric([f for f in listdir(path)
                                if isfile(join(path, f))
                                and (f.lower().endswith('.png')
                                     or (f.lower().endswith('.jpg'))
                                     or (f.lower().endswith('.jpeg'))
                                )])

    i = 0
    offset = args.offset
    for file in files:
        ignore = False
        ok = False
        if file in args.ignore:
            ignore = True
            ok = True
        img = cv2.imread(join(path,file))
        while not ok:
            (l,r) = cut(img, offset)
            if args.interactive:
                cv2.imshow('left', l)
                cv2.imshow('right', r)
                cv2.waitKey(1)
                read = prompt(file)
                if read == 'ignore': ignore = True ; break
                try: offset = int(read)
                except: ok = not read;
        if ignore:
            i += 1
        else:
            # cv2.imwrite(join(path,str(i)+'.jpg'),imgcrop)
            i += 2
