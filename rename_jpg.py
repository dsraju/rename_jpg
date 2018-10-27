#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem:
Often lot of times the jpeg files named by camera does not include the
date and time of the picture taken. When collected lot of files, having
date and time make it more valuable.

Solution:
Rename all the jpeg files based on the datetime of the file.
It rename all the files, recurlivel in a given directory.
 Default is the current directory.

1.0.1 (2018-10-18 01:03:56 PDT)
* Fixed an issue where the jpg files with missing exif data.
* Fixed an issue where the jpg file size is zero.
"""

__author__ = "Raju Dantuluri"
__license__ = "GPL"
__version__ = "1.0.1"

import sys
import argparse
import pathlib
import glob
from PIL import Image
#from PIL.ExifTags import TAGS


class Imageproc():
    '''Image processing module.

    To rename the jpeg files based on the datetime stamp found in exiv2 meta
    data in the image file header.
    '''

    def __init__(self, directory='.', verbose=False):
        self.dir = directory
        self.verbose = verbose
        self._count = 0

    def rename_jpg_datetime(self):
        '''Find all the files recursively in the directory and rename
        all the files based on the DateTimeDigitized found in the jpeg
        file(s).

        Arguments:
        ---------
        None.

        Example:
            IMG_001.JPG to be renamed 20180902293635.jpg
        '''
        types = ('*.jpg', '*.JPG', '*.jpeg', '*.JPEG')
        for ext in types:
            for file in glob.iglob(f'{self.dir}/**/{ext}', recursive=True):
                src_file = pathlib.Path(file)
                if src_file.stat().st_size == 0:
                    print(f'{src_file}: empty file')
                    continue
                datetm = None
                with Image.open(src_file) as imgfd:
                    exif = imgfd._getexif()
                    datetm = exif[36868] if exif and 36868 in exif else None
                if datetm is None:
                    print(f'{src_file}: found no exif data')
                    continue
                datetm = datetm.replace(' ', '')
                datetm = datetm.replace(':', '')
                dest_file = src_file.parent / f'{datetm}.jpg'
                if src_file == dest_file:
                    continue
                if dest_file.exists():
                    if self.verbose:
                        print(
                            f"skip - src:{src_file} dest:{dest_file} exists")
                    continue
                src_file.rename(dest_file)
                self._count += 1
                print(f'{file} => {dest_file}')
        print(f'Renamed files: {self._count}.')


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print('{} not supported.'.format(sys.version))
        sys.exit()
    PARSER = argparse.ArgumentParser(description='Process jpg image files.')
    PARSER.add_argument('--directory', required=False, default='.')
    PARSER.add_argument('--verbose', action="store_true", default=False)
    ARGS = PARSER.parse_args()
    IMG = Imageproc(directory=ARGS.directory, verbose=ARGS.verbose)
    IMG.rename_jpg_datetime()
