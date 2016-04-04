#!/usr/bin/env python3
#
# Script Name	: rename_jpg.py
# Author: Raju Dantuluri
# Created: 2016 03 15
# Version: 0.3

# Description: Rename jpg files to yyyymmddHHMMSS.jpg format.
# Also find out the duplicates to remove

import sys
import os
import collections
import re
import exifread
import datetime
import argparse
import hashlib


# get date and time from jpg file
def getDateTime(fpath):
    dt = None
    f = open(fpath, 'rb')
    # Read Exif tags
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            if tag == "EXIF DateTimeOriginal":
                d = datetime.datetime.strptime(str(tags[tag]), "%Y:%m:%d %H:%M:%S")
                dt = '{:%Y%02m%02d%H%M%S}.jpg'.format(d)
                if len(dt) != len("yyyymmddHHMMSS.jpg"):
                    dt = None
    return dt

# Rename the jpg file to dateTime format (ex:yyyymmddhhmmss.jpg)
def renameFile(topDir):
    for dirpath, dirnames, filenames in os.walk(topDir):
        for f in filenames:
            origFile = os.path.join(dirpath,f)
            if (f.lower().endswith(".jpg")):
                datetimeJpg = getDateTime(origFile)
                if datetimeJpg is None:
                    print("%s failed to extract dateTime" % (origFile))
                    continue
                newFile = os.path.join(dirpath,datetimeJpg)
                if not os.path.exists(newFile):
                    # newFile does not exist, safe to rename
                    os.rename(origFile, newFile)

# Delete duplicate files using md5 checksum
def deleteDups(topDir, delDups):
    md5hash = {}
    for dirpath, dirnames, filenames in os.walk(topDir):
        for f in filenames:
            origFile = os.path.join(dirpath,f)
            if (f.lower().endswith(".jpg")):
                filehash = hashlib.md5(open(origFile,'rb').read()).hexdigest()
                if md5hash.get(filehash) is None:
                    md5hash[filehash] = origFile
                elif delDups == "Yes":
                    os.remove(origFile)
                    print("%s deleted a duplicate of %s" % (origFile,md5hash.get(filehash)))
                else:
                    print("%s is a duplicate of %s" % (origFile,md5hash.get(filehash)))

def main():
    parser = argparse.ArgumentParser(description=
             'Rename jpg image files to dateTime.jpg format.')
    dstHelpTxt="Destination directory to rename jpg files (default: current directory)"
    delHelpTxt="Delete duplicate files, Yes to delete (default: No)"
    parser.add_argument('--destination', default=".", help=dstHelpTxt)
    parser.add_argument('--delete_duplicates', default="No", help=delHelpTxt)
    topDir = vars(parser.parse_args())['destination']
    delDups = vars(parser.parse_args())['delete_duplicates']
    renameFile(topDir)
    deleteDups(topDir, delDups)

if __name__ == "__main__":
    main()

