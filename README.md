# batch-file-manage-python

Contains a set of scripts to enable processing of batches of files, in particular images (e.g., mangas or comics collections).

## Prerequirements

Scripts use `os`, `shutil`, `argparse`, `PIL` and `matplotlib`.
If available in python env, will load `argcomplete` for autocomplete.


## Installation

Install with pip:
```
pip install .
```

## Description of scripts

##### CBZ

Zip all folders in working directory and rename them to .cbz.

##### Crop

Crop bands of pixels from images.

##### Cut

Cut images in half (vertically).

##### Move

Move all files from subfolders into working directory.

##### Number

Rename all images with increasing indices.

##### Remove

Remove all files with a given string in the name.

##### Rename

Rename all folders and append increasing increasing.
