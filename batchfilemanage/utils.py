import re
from os import listdir
from os.path import isfile, isdir, join, exists
import shutil


def prompt(message, values=None):
    """Prompt a message and return the user input.
    Set values to None for binary input ('y' or 'n'), to 0 for integer input, or to a list of possible inputs.
    """
    if values is None:
        message += ' (y/n)'
    message += ' > '
    while 1:
        ans = input(message)
        if values is None:
            if ans == 'y':
                return True
            elif ans == 'n':
                return False
        elif values == 0:
            try:
                read = int(ans)
            except:
                continue
            return read
        elif ans in values:
            return ans


def get_extension(file):
    """Return the extension of the given filename."""
    return file.split('.')[-1]


def sorted_aphanumeric(path, ext=[], ignore=[], dirs=False):
    """Alphanumeric sort all files in path.
    Only consider extensions in ext, ignore filenames in ignore, and list only directions if dirs.
    """
    data = [
        f
        for f in listdir(path)
        if (not dirs and isfile(join(path, f)))
        or (dirs and isdir(join(path, f)))
        and f not in ignore
        and (ext == [] or get_extension(f.lower()) in ext)
    ]
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def remove_folder(path, check_empty=False, verbose=False):
    """Delete the target folder path.
    Returns:    0   target deleted
                -1  target does not exist
                -2  target not a directory
                -3  target not empty
    """
    # check if folder exists
    if exists(path):
        if not isdir(path):
            if verbose:
                print('Target %s is not a directory' % path)
            return -2
        if not check_empty or listdir(path) == []:
            shutil.rmtree(path)
            if verbose:
                print('Folder %s deleted' % path)
            return 0
        else:
            if verbose:
                print('Folder %s is not empty' % path)
            return -3
    else:
        if verbose:
            print('Folder %s does not exist' % path)
        return -1
