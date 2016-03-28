#!/usr/bin/env python3
#
import os
import sys
import collections
import re
import exifread
import datetime
import argparse

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
def renameFile(topDir, delDups):
    for dirpath, dirnames, filenames in os.walk(topDir):
        for f in filenames:
            origFile = os.path.join(dirpath,f)
            if (f.lower().endswith(".jpg")):
                datetimeJpg = getDateTime(origFile)
                newFile = os.path.join(dirpath,datetimeJpg)
                if not os.path.exists(newFile):
                    print("doent exists %s %s" % (origFile, newFile))
                    os.rename(origFile, newFile)
                elif origFile != newFile and os.path.exists(newFile):
                    if delDups == "Yes":
                        os.remove(origFile)
                        print("%s is a duplicate TOBE DELETED" % (origFile))
                    else:
                        print("%s is a duplicate of %s" % (origFile, newFile))

def main():
    parser = argparse.ArgumentParser(description=
             'Rename jpg image files to dateTime.jpg format.')
    dstHelpTxt="Destination directory to rename jpg files (default: current directory)"
    delHelpTxt="Delete duplicate files, Yes to delete (default: No)"
    parser.add_argument('--destination', default=".", help=dstHelpTxt)
    parser.add_argument('--delete_duplicates', default="No", help=delHelpTxt)
    topDir = vars(parser.parse_args())['destination']
    delDups = vars(parser.parse_args())['delete_duplicates']
    renameFile(topDir, delDups)

if __name__ == "__main__":
    main()

