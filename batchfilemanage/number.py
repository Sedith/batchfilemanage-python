#!/usr/bin/python3
import argparse
from PIL import Image
from os import rename
from os.path import join, exists
from batchfilemanage.utils import sorted_aphanumeric, get_ext


## command description line
desc = 'rename all images with increasing indices'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('number', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-i', dest='index', help='starting index', default=1, type=int)
    parser.add_argument('-d', dest='digits', help='number of digits', default=3, choices=[2, 3], type=int)
    parser.add_argument('-r', dest='recursive', help='recursively number in all subdirectories', action='store_true')
    parser.add_argument('-k', dest='keepindex', help='recursively number in all subdirectories without reseting index', action='store_true')
    parser.add_argument('-g', dest='gap', help='gap between each successive index', default=1, type=int)
    parser.add_argument('-t', dest='test', help='test mode (no actual renaming)', action='store_true')

    return parser


def number_folder(path, index):
    ## get list of images
    images = sorted_aphanumeric(path, ignore=args.ignore, ext=['jpg', 'png', 'jpeg'])

    print('Renaming in directory %s' % dir)
    names = []
    for file in images:
        ## get file extension
        ext = get_ext(file).lower()
        if ext in ['jpg', 'jpeg']:
            ext = '.jpg'
        elif ext == 'png':
            ext = '.png'

        ## create new filename
        (w, h) = Image.open(join(path, file)).size
        if w > h:
            if args.digits == 2:
                name = "%02d-%02d" % (index, index + 1) + ext
            elif args.digits == 3:
                name = "%03d-%03d" % (index, index + 1) + ext
            index += args.gap+1
        else:
            if args.digits == 2:
                name = "%02d" % index + ext
            elif args.digits == 3:
                name = "%03d" % index + ext
            index += args.gap

        ## renaming to temporary name
        if file == name:
            continue
        print('Renaming %s -> %s' % (file, name))
        names += [name]
        if not args.test:
            rename(join(path, file), join(path, 'tmp' + name))

    ## renaming to final name
    if not args.test:
        for name in names:
            rename(join(path, 'tmp' + name), join(path, name))

    return index


def main(args):
    if args.recursive or args.keepindex:
        ## get list of directories in path
        dirs = sorted_aphanumeric(args.path, dirs=True)

        index = args.index
        for dir in [join(args.path, d) for d in dirs]:
            if not args.keepindex:
                index = args.index
            index = number_folder(dir, index)
    else:
        number_folder(args.path, args.index)


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
