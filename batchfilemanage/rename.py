#!/usr/bin/python3
import argparse
from os import rename
from os.path import join, exists
from batchfilemanage.utils import sorted_aphanumeric


## command description line
desc = 'rename all folders and append increasing increasing'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('rename', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(dest='name', help='base name for renaming', type=str)
    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-i', dest='index', help='starting index', default=1, type=int)
    parser.add_argument('-d', dest='digits', help='number of digits', default=2, choices=[2, 3], type=int)
    parser.add_argument('-t', dest='test', help='test mode (no actual renaming)', action='store_true')

    return parser


def main(args):
    ## get list of directories
    dirs = sorted_aphanumeric(args.path, dirs=True)

    names = []
    for dir in dirs:
        ## create new dirname
        if args.digits == 2:
            name = args.name + " %02d" % args.index
        elif args.digits == 3:
            name = args.name + " %03d" % args.index
        args.index += 1

        ## renaming to temporary name
        if dir == name:
            continue
        print('Renaming %s -> %s' % (dir, name))
        names += [name]
        if not args.test:
            rename(join(args.path, dir), join(args.path, 'tmp' + name))

    ## renaming to final name
    if not args.test:
        for name in names:
            rename(join(args.path, 'tmp' + name), join(args.path, name))


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
