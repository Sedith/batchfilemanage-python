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
args = parser.parse_args()

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

if __name__ == '__main__':
    path = args.path
    pos = args.pos
    pix = args.pix
    files = sorted_aphanumeric([f for f in listdir(path)
                                if isfile(join(path, f))
                                and (f.lower().endswith('.png')
                                     or (f.lower().endswith('.jpg'))
                                     or (f.lower().endswith('.jpeg'))
                                )])
    for file in files:
        img = cv2.imread(join(path,file))
        if pos == 'left':
            imgcrop = img[:,pix:-1]
        if pos == 'top':
            imgcrop = img[pix:-1,:]
        if pos == 'right':
            imgcrop = img[:,0:-pix]
        if pos == 'bottom':
            imgcrop = img[0:-pix,:]
        imgcrop = img[0:-pix,:]
        if args.test:
            img = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)
            imgcrop = cv2.resize(imgcrop,(0,0),fx = 0.5,fy = 0.5)
            cv2.imshow('1',img)
            cv2.imshow('2',imgcrop)
            cv2.waitKey(0)
        else:
            cv2.imwrite(join(path,file),imgcrop)
