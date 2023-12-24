#!/usr/bin/python3
import argparse
import cv2
from os.path import join
from batchfilemanage.utils import sorted_aphanumeric, prompt


parser = argparse.ArgumentParser(description='Crop images.')
parser.add_argument(dest='pix', help='Number of pixels to crop.', type=int)
parser.add_argument(dest='pos', help='Location of pixels to crop (top, right, bottom, left).', choices=['top', 'right', 'bottom', 'left'], type=str)
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-n', dest='ignore', help='Filenames of images to ignore.', default=[], type=str, nargs='*')
parser.add_argument('-i', dest='interactive', help='Interactive mode.', action='store_true')
parser.add_argument('-r', dest='resize', help='Resize factor for display.', default=0.5, type=float)
args = parser.parse_args()


def crop(img, pos, pix):
    if pos == 'left':
        imgcrop = img[:, pix:-1]
    if pos == 'top':
        imgcrop = img[pix:-1, :]
    if pos == 'right':
        imgcrop = img[:, 0:-pix]
    if pos == 'bottom':
        imgcrop = img[0:-pix, :]
    return imgcrop


if __name__ == '__main__':
    path = args.path
    pix = args.pix

    for file in sorted_aphanumeric(path, ignore=args.ignore, ext=['jpg', 'png', 'jpeg']):
        img = cv2.imread(join(path, file))
        imgcrop = crop(img, args.pos, pix)
        save = True
        if args.interactive:
            stop = False
            while not stop:
                cv2.imshow('original', cv2.resize(img, (0, 0), fx=args.resize, fy=args.resize))
                cv2.imshow('cropped', cv2.resize(imgcrop, (0, 0), fx=args.resize, fy=args.resize))
                cv2.waitKey(2)
                ans = prompt('%s - (o)k/(i)gnore/(r)ecrop/(a)ll/(c)ancel' % file, ['o', 'i', 'r', 'a', 'c'])
                if ans == 'o':
                    stop = True
                    save = True
                elif ans == 'i':
                    stop = True
                    save = False
                elif ans == 'r':
                    pix = prompt('new crop value', 0)
                    imgcrop = crop(img, args.pos, pix)
                elif ans == 'a':
                    args.interactive = False
                    stop = True
                elif ans == 'c':
                    exit()
        if save or not args.interactive:
            print('Cropping %s of %i pixels at %s' % (file, pix, args.pos))
            cv2.imwrite(join(path, file), imgcrop)
