#!/usr/bin/python3
import argparse
from os import listdir, remove
from os.path import isfile, isdir, join
from batchfilemanage.utils import remove_folder


## command description line
desc = 'remove all files with a given string in the name'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('remove', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(dest='word', help='word to remove', type=str)
    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-i', dest='interactive', help='interactive prompt', action='store_true')
    parser.add_argument('-d', dest='dirs', help='delete directories as well', action='store_true')
    parser.add_argument('-r', dest='recursive', help='recursively run in all the subfolder tree', action='store_true')

    return parser



def removing(path, args):
    ## get list of files
    files = listdir(path)

    for file in files:
        if args.word in file:
            if isfile(join(path, file)) and (not args.interactive or (args.interactive and prompt('Delete %s?' % file))):
                print('Removing file %s' % join(path, file))
                remove(join(path, file))
            elif args.dirs and (not args.interactive or (args.interactive and prompt('Delete %s?' % file))):
                print('Removing directory %s' % join(path, file))
                remove_folder(join(path, file))
        if args.recursive and isdir(join(path, file)):
            removing(join(path, file), args.word)


def main(args):
    removing(args.path, args)


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
