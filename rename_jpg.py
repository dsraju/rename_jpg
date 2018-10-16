#!/usr/bin/env python
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
"""

__author__ = "Raju Dantuluri"
__license__ = "GPL"
__version__ = "1.0.0"

import pathlib
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import argparse


class Imageproc():
    '''Image processing module.

    To rename the jpeg files based on the datetime stamp found in exiv2 meta
    data in the image file header.
    '''

    def __init__(self, directory='.', verbose=False):
        self.dir = directory
        self.verbose = verbose

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
        for f in types:
            filelist = list(glob.iglob(f'{self.dir}/**/{f}', recursive=True))
            if len(filelist):
                for file in filelist:
                    src_file = pathlib.Path(file)
                    img = Image.open(src_file)
                    dt = img._getexif()[36868]
                    img.close()
                    del img
                    dt = dt.replace(' ', '')
                    dt = dt.replace(':', '')
                    dest_file = src_file.parent / f'{dt}.jpg'
                    if src_file == dest_file:
                        continue
                    if dest_file.exists():
                        if self.verbose:
                            print(
                                f"skip - src:{src_file} dest:{dest_file} exists")
                        continue
                    src_file.rename(dest_file)
                    print(f'{file} => {dest_file}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process image files.')
    parser.add_argument('--directory', required=False, default='.')
    parser.add_argument('--verbose', action="store_true", default=False)
    args = parser.parse_args()
    img = Imageproc(directory=args.directory, verbose=args.verbose)
    img.rename_jpg_datetime()
