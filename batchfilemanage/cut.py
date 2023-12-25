#!/usr/bin/python3
import argparse
import cv2
from os import remove
from os.path import join
from batchfilemanage.utils import sorted_aphanumeric, prompt, remove_ext, get_ext
import matplotlib.pyplot as plt


## command description line
desc = 'Cut images in half (vertically).'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('cut', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
    parser.add_argument('-d', dest='delete', help='Delete source file after cutting.', action='store_true')
    parser.add_argument('-i', dest='interactive', help='Interactive prompt.', action='store_true')
    parser.add_argument('-s', dest='direction', help='Reading direction (lr: left to write; rl: right to left)', default='rl', type=str, choices=['lr', 'rl'])
    parser.add_argument('-n', dest='ignore', help='Filenames of images to ignore.', default=[], type=str, nargs='*')
    parser.add_argument('-o', dest='offset', help='Offset in pixels (positive to the right).', default=0, type=int)
    parser.add_argument('-r', dest='resize', help='Resize factor for display (in interactive mode).', default=0.5, type=float)

    return parser


def cut(img, offset):
    half = round(img.shape[1] / 2) + offset
    left = img[:, 0:half]
    right = img[:, half + 1 : -1]
    return (left, right)


def main(args):
    ## get list of images
    images = sorted_aphanumeric(args.path, ignore=args.ignore, ext=['jpg', 'png', 'jpeg'])

    for file in images:
        img = cv2.imread(join(args.path, file))
        (l, r) = cut(img, args.offset)
        save = True

        if args.interactive:
            fig = None

            while 1:
                ## check that figure is still open
                if not fig or not plt.fignum_exists(fig.number):
                    fig = plt.figure('cropping')
                fig.clear()
                ax = [fig.add_subplot(121), fig.add_subplot(122)]
                ax[0].get_yaxis().set_visible(False)
                ax[1].get_yaxis().set_visible(False)
                ax[0].set_xlabel('left image')
                ax[1].set_xlabel('right image')
                ax[0].imshow(l)
                ax[1].imshow(r)
                plt.show(block=False)
                
                ans = prompt('%s - (o)k/(i)gnore/(r)ecut/(a)ll/(c)ancel' % file, ['o', 'i', 'r', 'a', 'c'])
                if ans == 'o':
                    save = True
                    break
                elif ans == 'i':
                    save = False
                    break
                elif ans == 'r':
                    args.offset = prompt('new offset value', 0)
                    (l, r) = cut(img, args.offset)
                elif ans == 'a':
                    args.interactive = False
                    break
                elif ans == 'c':
                    exit()

        if save:
            print('Cutting %s with offset of %i' % (file, args.offset))
            file_noext = remove_ext(file)
            ext = get_ext(file)
            if args.direction == 'rl': # right side then left side
                cv2.imwrite(join(args.path, file_noext + '_1.' + ext), r)
                cv2.imwrite(join(args.path, file_noext + '_2.' + ext), l)
            else:
                cv2.imwrite(join(args.path, file_noext + '_2.' + ext), r)
                cv2.imwrite(join(args.path, file_noext + '_1.' + ext), l)
            if args.delete:
                remove(join(args.path, file))


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
