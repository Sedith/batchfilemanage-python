#!/usr/bin/python3
import argparse
from PIL import Image
from os import rename
from os.path import join, exists
from batchfilemanage.utils import sorted_aphanumeric, get_ext


def numerotage(path, index):
    names = []
    for file in sorted_aphanumeric(path, ext=['jpg', 'png', 'jpeg']):
        # File extension
        ext = get_ext(file).lower()
        if ext in ['jpg', 'jpeg']:
            ext = '.jpg'
        elif ext == 'png':
            ext = '.png'
        # New filename
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
        # Renaming to temporary name
        if file == name:
            continue
        print('Renaming %s -> %s' % (file, name))
        names += [name]
        if not args.test:
            rename(join(path, file), join(path, 'tmp' + name))
    # Renaming to final name
    if not args.test:
        for name in names:
            rename(join(path, 'tmp' + name), join(path, name))
    print('Done')
    return index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Number images in directory (jpgs and pngs).')
    parser.add_argument('-i', dest='index', help='Index to start with.', default=1, type=int)
    parser.add_argument('-p', dest='path', help='Path to working directory.', default='./', type=str)
    parser.add_argument('-d', dest='digits', help='Number of digits.', default=3, choices=[2, 3], type=int)
    parser.add_argument('-R', dest='recursive', help='Recursively number all subdirectories.', action='store_true')
    parser.add_argument('-k', dest='keepindex', help='Recursively number all subdirectories without reseting index.', action='store_true')
    parser.add_argument('-g', dest='gap', help='Gap between each successive index.', default=1, type=int)
    parser.add_argument('-t', dest='test', help='Test mode (no actual renaming).', action='store_true')
    args = parser.parse_args()

    if args.recursive or args.keepindex:
        index = args.index
        for dir in [join(args.path, d) for d in sorted_aphanumeric(args.path, dirs=True)]:
            print('Renaming in directory %s' % dir)
            if not args.keepindex:
                index = args.index
            index = numerotage(dir, index)
    else:
        numerotage(args.path, args.index)
