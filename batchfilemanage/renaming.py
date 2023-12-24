#!/usr/bin/python3
import argparse
from os import rename
from os.path import join, exists
from batchfilemanage.utils import sorted_aphanumeric


parser = argparse.ArgumentParser(description='Rename folders as with increasing numbers.')
parser.add_argument(dest='name', help='Base name for renaming.', type=str)
parser.add_argument('-i', dest='index', help='Index to start with.', default=1, type=int)
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-d', dest='digits', help='Number of digits.', default=2, choices=[2, 3], type=int)
parser.add_argument('-t', dest='test', help='Test mode.', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    path = args.path
    index = args.index

    dirs = sorted_aphanumeric(args.path, dirs=True)
    names = []
    for dir in dirs:
        # New dirname
        if args.digits == 2:
            name = args.name + " %02d" % index
        elif args.digits == 3:
            name = args.name + " %03d" % index
        index += 1
        # Renaming to temporary name
        if dir == name:
            continue
        print('Renaming %s to %s' % (dir, name))
        names += [name]
        if not args.test:
            rename(join(path, dir), join(path, 'tmp' + name))
    # Renaming to final name
    if not args.test:
        for name in names:
            rename(join(path, 'tmp' + name), join(path, name))
    print('Done')
