import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='batch-file-manage-python',
    version='1.0',
    packages=setuptools.find_packages(),
    scripts=[
        'batchfilemanage/cbzing.py',
        'batchfilemanage/cropping.py',
        'batchfilemanage/cutting.py',
        'batchfilemanage/moving.py',
        'batchfilemanage/numbering.py',
        'batchfilemanage/renaming.py',
    ],
    author="Martin Jacquet",
    author_email="martin.jacquet@posteo.net",
    description="Batch images file managing tools for mangas and comics collections.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sedith/batch-file-manage-python",
    license='The Unlicense',
)
