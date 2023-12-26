#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
from os.path import join
from batchfilemanage.utils import sorted_aphanumeric, prompt


## command description line
desc = 'crop bands of pixels from images'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('crop', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(dest='pix', help='number of pixels to crop', type=int)
    parser.add_argument(dest='pos', help='location of pixels to crop (top, right, bottom, left)', choices=['top', 'right', 'bottom', 'left'], type=str)
    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-d', dest='delete', help='delete source file after cutting', action='store_true')
    parser.add_argument('-i', dest='interactive', help='interactive prompt', action='store_true')
    parser.add_argument('-n', dest='ignore', help='filenames of images to ignore', default=[], type=str, nargs='*')

    return parser


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


def main(args):
    ## get list of images
    images = sorted_aphanumeric(args.path, ignore=args.ignore, ext=['jpg', 'png', 'jpeg'])

    for file in images:
        img = plt.imread(join(args.path, file))
        imgcrop = crop(img, args.pos, args.pix)
        save = True

        if args.interactive:
            fig = None

            while 1:
                ## check that figure is still open
                if not fig or not plt.fignum_exists(fig.number):
                    fig = plt.figure('cropping')
                fig.clear()
                ax = [fig.add_subplot(121), fig.add_subplot(122)]
                ax[0].set_xlabel('original')
                ax[1].set_xlabel('cropped')
                ax[0].imshow(img)
                ax[1].imshow(imgcrop)
                plt.show(block=False)

                ans = prompt('%s - (o)k/(i)gnore/(r)ecrop/(a)ll/(c)ancel' % file, ['o', 'i', 'r', 'a', 'c'])
                if ans == 'o':
                    save = True
                    break
                elif ans == 'i':
                    save = False
                    break
                elif ans == 'r':
                    args.pix = prompt('new crop value', 0)
                    imgcrop = crop(img, args.pos, args.pix)
                elif ans == 'a':
                    args.interactive = False
                    break
                elif ans == 'c':
                    exit()

        if save:
            print('Cropping %s of %i pixels at %s' % (file, args.pix, args.pos))
            file_noext = remove_ext(file)
            ext = get_ext(file)
            plt.imsave(join(args.path, file_noext + '_crop.' + ext), imgcrop)
            if args.delete:
                remove(join(args.path, file))


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
