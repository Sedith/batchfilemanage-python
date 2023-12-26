#!/usr/bin/python3
import argparse
from os import listdir, remove
from os.path import isdir, join, exists
from shutil import move
from batchfilemanage.utils import sorted_aphanumeric, prompt, remove_folder


## command description line
desc = 'move files from subfolders into working directory'

def create_args(subparsers=None):
    if subparsers:
        parser = subparsers.add_parser('move', description=desc, help=desc)
    else:
        parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-p', dest='path', help='path to working directory', default='./', type=str)
    parser.add_argument('-d', dest='delete', help='delete folder after moving its content', action='store_true')
    parser.add_argument('-i', dest='interactive', help='interactive prompt', action='store_true')
    parser.add_argument('-c', dest='current', help='move all files from the current working directory to its parent', action='store_true')
    parser.add_argument('-r', dest='recursive', help='recursively run in all the subfolders of working directory (one level only)', action='store_true')

    return parser


def move_dir_content(dir):
    ## get parent folder path
    target = join(dir, '..')
    ## get list of files
    files = listdir(path)

    for file in files:
        if not args.interactive or prompt('Move %s?' % join(dir, file)):
            print('Moving %s to %s' % (join(dir, file), join(target, file)))
            if exists(join(target, file)):
                ans = prompt('%s already exists: (o)verwrite/(r)ename/(s)kip?' % join(target, file), ['o', 'r', 's'])
                if ans == 's':
                    continue
                elif ans == 'r':
                    print('Renaming to %s' % 'new_' + file)
                    move(join(dir, file), join(target, 'new_' + file))
                elif ans == 'o':
                    if isfile(join(target, file)):
                        remove(join(target, file))
                    else:
                        remove_folder(join(target, file))
                    move(join(dir, file), join(target, file))
            else:
                move(join(dir, file), join(target, file))

    if args.delete and (not args.interactive or prompt('Delete %s?' % dir)):
        remove_folder(dir, verbose=True)


def main(args):
    if args.current:
        move_dir_content(args.path)
    elif args.recursive:
        dirs = sorted_aphanumeric(args.path, dirs=True)
        for dir in [join(args.path, d) for d in dirs]:
            subdirs = sorted_aphanumeric(dir, dirs=True)
            for subdir in [join(dir, sd) for sd in subdirs]:
                move_dir_content(subdir)
    else:
        dirs = sorted_aphanumeric(args.path, dirs=True)
        for dir in [join(args.path, d) for d in dirs]:
            move_dir_content(dir)


if __name__ == '__main__':
    parser = create_args()
    args = parser.parse_args()
    main(args)
