#!/usr/bin/python3
import argparse
from os import getcwd
from os.path import join, exists
from shutil import make_archive, move
from batchfilemanage.utils import sorted_aphanumeric, remove_folder, prompt


## command description line
desc = 'zip all folders in working directory and rename them to .cbz'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('cbz', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-d', dest='delete', help='delete folders after cbzing', action='store_true')
    parser.add_argument('-i', dest='interactive', help='interactive prompt', action='store_true')

    return parser


def main(args):
    ## get list of directories
    dirs = sorted_aphanumeric(args.path, dirs=True)

    for dir in dirs:
        if not args.interactive or prompt('Cbz %s?' % dir):
            ## check if the cbz already exists
            if exists(join(args.path, dir, '.cbz')):
                print('Skipping: cbz file already exists in working directory')
                continue

            ## create archive
            if not exists(join(args.path, dir, '.zip')):
                print('Cbzing %s' % dir)
                make_archive(dir, 'zip', join(getcwd(), args.path), dir)

            ## rename to .cbz
            move(dir + '.zip', join(args.path, dir + '.cbz'))

            ## delete folder
            if args.delete and (not args.interactive or prompt('Delete %s?' % dir)):
                print('Removing %s' % dir)
                remove_folder(join(args.path, dir))


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
