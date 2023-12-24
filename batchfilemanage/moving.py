#!/usr/bin/python3
import argparse
from os import listdir, remove
from os.path import isdir, join, exists
from shutil import move
from batchfilemanage.utils import sorted_aphanumeric, prompt, remove_folder


parser = argparse.ArgumentParser(description='Move all files contained in subfolders in working directory.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-i', dest='prompt', help='Prompt before moving.', action='store_true')
parser.add_argument('-c', dest='current', help='Move all files from the current working directory to its parent.', action='store_true')
parser.add_argument('-R', dest='recursive', help='Run in all the subfolders of working directory.', action='store_true')
parser.add_argument('-d', dest='delete', help='Delete folder after moving its content.', action='store_true')
args = parser.parse_args()


def moving(dir):
    target = join(dir, '..')
    for file in listdir(dir):
        if not args.prompt or prompt('Moving %s?' % join(dir, file)):
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
    if args.delete and (not args.prompt or prompt('Delete %s?' % dir)):
        remove_folder(dir, verbose=True)


if __name__ == '__main__':
    path = args.path
    if args.current:
        moving(path)
    elif args.recursive:
        for dir in [join(path, d) for d in sorted_aphanumeric(path, dirs=True)]:
            for subdir in [join(dir, d) for d in sorted_aphanumeric(dir, dirs=True)]:
                moving(subdir)
    else:
        for dir in [join(path, d) for d in sorted_aphanumeric(path, dirs=True)]:
            moving(dir)
