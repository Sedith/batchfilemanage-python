#!/usr/bin/python3
import argparse
import cv2
from os import remove
from os.path import join
from batchfilemanage.utils import sorted_aphanumeric, prompt, remove_ext, get_ext


parser = argparse.ArgumentParser(description='Cut images in half.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-s', dest='direction', help='Reading direction (lr: left to write; rl: right to left)', default='rl', type=str, choices=['lr', 'rl'])
parser.add_argument('-i', dest='interactive', help='Display and prompt for each image.', action='store_true')
parser.add_argument('-d', dest='delete', help='Delete source file after cutting.', action='store_true')
parser.add_argument('-n', dest='ignore', help='Filenames of images to ignore.', default=[], type=str, nargs='*')
parser.add_argument('-o', dest='offset', help='Offset in pixels (positive to the right).', default=0, type=int)
parser.add_argument('-r', dest='resize', help='Resize factor for display.', default=0.5, type=float)
args = parser.parse_args()


def cut(img, offset):
    half = round(img.shape[1] / 2) + offset
    left = img[:, 0:half]
    right = img[:, half + 1 : -1]
    return (left, right)


if __name__ == '__main__':
    path = args.path

    offset = args.offset
    for file in sorted_aphanumeric(path, ignore=args.ignore, ext=['jpg', 'png', 'jpeg']):
        img = cv2.imread(join(path, file))
        save = True
        (l, r) = cut(img, offset)
        if args.interactive:
            stop = False
            while not stop:
                cv2.imshow('left', cv2.resize(l, (0, 0), fx=args.resize, fy=args.resize))
                cv2.imshow('right', cv2.resize(r, (0, 0), fx=args.resize, fy=args.resize))
                cv2.waitKey(100)
                ans = prompt('%s - (o)k/(i)gnore/(r)ecut/(a)ll/(c)ancel' % file, ['o', 'i', 'r', 'a', 'c'])
                if ans == 'o':
                    stop = True
                    save = True
                elif ans == 'i':
                    stop = True
                    save = False
                elif ans == 'r':
                    offset = prompt('new offset value', 0)
                    (l, r) = cut(img, offset)
                elif ans == 'a':
                    args.interactive = False
                    stop = True
                elif ans == 'c':
                    exit()
        if save:
            print('Cutting %s with offset of %i' % (file, offset))
            file_noext = remove_ext(file)
            ext = get_ext(file)
            if args.direction == 'rl': # right side then left side
                cv2.imwrite(join(path, file_noext + '_1.' + ext), r)
                cv2.imwrite(join(path, file_noext + '_2.' + ext), l)
            else:
                cv2.imwrite(join(path, file_noext + '_2.' + ext), r)
                cv2.imwrite(join(path, file_noext + '_1.' + ext), l)
            if args.delete:
                remove(join(path, file))
