#!/usr/bin/python3
import argparse
from os import listdir, remove
from os.path import isfile, isdir, join
from batchfilemanage.utils import remove_folder


parser = argparse.ArgumentParser(description='Remove all files with a given string in the name.')
parser.add_argument(dest='word', help='Word to remove.', type=str)
parser.add_argument('-R', dest='recursive', help='Recursively remove in all subfolders.', action='store_true')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-i', dest='prompt', help='Prompt before removing.', action='store_true')
parser.add_argument('-d', dest='dirs', help='Delete directories as well.', action='store_true')
args = parser.parse_args()


def removage(path, word):
    files = listdir(path)
    for file in files:
        if word in file:
            if isfile(join(path, file)) and (not args.prompt or (args.prompt and prompt('Delete %s?' % file))):
                print('Removing file %s' % join(path, file))
                remove(join(path, file))
            elif args.dirs and (not args.prompt or (args.prompt and prompt('Delete %s?' % file))):
                print('Removing directory %s' % join(path, file))
                remove_folder(join(path, file))
        if args.recursive and isdir(join(path, file)):
            removage(join(path, file), word)


if __name__ == '__main__':
    removage(args.path, args.word)
