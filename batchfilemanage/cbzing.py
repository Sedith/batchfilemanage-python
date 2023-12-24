#!/usr/bin/python3
import argparse
from os import getcwd
from os.path import join, exists
from shutil import make_archive, move
from batchfilemanage.utils import sorted_aphanumeric, remove_folder, prompt


parser = argparse.ArgumentParser(description='Zip all folders in working directory and rename them to .cbz.')
parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
parser.add_argument('-d', dest='delete', help='Delete folders after cbzing.', action='store_true')
parser.add_argument('-i', dest='prompt', help='Prompt before every cbzing and removal.', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    path = args.path

    dirs = sorted_aphanumeric(args.path, dirs=True)
    for dir in dirs:
        if not args.prompt or prompt('Cbzing %s?' % dir):
            if exists(join(path, dir, '.cbz')):
                print('Skipping: cbz file already exists in working directory')
                continue
            if not exists(join(path, dir, '.zip')):
                print('Cbzing %s' % dir)
                make_archive(dir, 'zip', join(getcwd(), path), dir)
            move(dir + '.zip', join(path, dir + '.cbz'))
            if args.delete and (not args.prompt or prompt('Delete %s?' % dir)):
                remove_folder(join(path, dir))
