#!/usr/bin/python3
import cv2
import argparse
from os import listdir, rename
from os.path import isfile, isdir, join, exists
import re

parser = argparse.ArgumentParser(description='Crop images.')
parser.add_argument(dest='pix', help='Number of pixels to crop.', type=int)
parser.add_argument(dest='pos', help='Location of pixels to crop (top, right, bottom, left).', choices=['top', 'right', 'bottom', 'left'], type=str)
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-t', dest='test', help='Test mode (display but no crop).', action='store_true')
parser.add_argument('-n', dest='ignore', help='Filenames of images to ignore.', default=[], type=str, nargs='*')
parser.add_argument('-i', dest='interative', help='Interactive mode.', action='store_true')
args = parser.parse_args()

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def crop(img, pos, pix):
    if pos == 'left':
        imgcrop = img[:,pix:-1]
    if pos == 'top':
        imgcrop = img[pix:-1,:]
    if pos == 'right':
        imgcrop = img[:,0:-pix]
    if pos == 'bottom':
        imgcrop = img[0:-pix,:]
    return imgcrop

def prompt(message, values = None):
    while(1):
        ans = input(message)
        if values == 0:
            try:    read = int(ans)
            except: continue
            return read
        elif values is None or ans in values:
            return ans

if __name__ == '__main__':
    path = args.path
    pos = args.pos
    pix = args.pix
    interactive = args.interative
    files = sorted_aphanumeric([f for f in listdir(path)
                                if isfile(join(path, f))
                                and f not in args.ignore
                                and (f.lower().endswith('.png')
                                     or (f.lower().endswith('.jpg'))
                                     or (f.lower().endswith('.jpeg'))
                                )])
    for file in files:
        img = cv2.imread(join(path,file))
        imgcrop = crop(img, pos, pix)
        if args.test:
            img = cv2.resize(img,(0,0),fx = 0.3,fy = 0.3)
            imgcrop = cv2.resize(imgcrop,(0,0),fx = 0.3,fy = 0.3)
            cv2.imshow('original',img)
            cv2.imshow('cropped',imgcrop)
            cv2.waitKey(0)
        if interactive:
            stop = False
            while not stop:
                img_d = cv2.resize(img,(0,0),fx = 0.3,fy = 0.3)
                imgcrop_d = cv2.resize(imgcrop,(0,0),fx = 0.3,fy = 0.3)
                cv2.imshow('original', img_d)
                cv2.imshow('cropped', imgcrop_d)
                cv2.waitKey(10)
                ans = prompt(file+' - ok? ((o)k/(i)gnore/(r)ecrop/(all) > ', ['o','i','r','a'])
                if ans == 'o':
                    stop = True
                    save = True
                elif ans == 'i':
                    stop = True
                    save = False
                elif ans == 'r':
                    pix = prompt('new crop value > ', 0)
                    imgcrop = crop(img, pos, pix)
                elif ans == 'a':
                    interactive = False
                    stop = True
        if (save or not interactive) and not args.test:
            cv2.imwrite(join(path,file),imgcrop)
