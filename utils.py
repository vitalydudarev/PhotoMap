import fnmatch
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json
import fileutils
import imageutils

EXTENSIONS = ('.jpg', '.jpeg', '.JPEG', '.JPG')
LIMIT = 30
THUMB_SIZE = 48, 48


def get_photo_data(folder_path, thumb_folder_path):
    files = fileutils.get_files(folder_path, EXTENSIONS)
    fileutils.create_directory(thumb_folder_path)

    res = []
    
    print 'total files: ' + str(len(files))

    for index, file_name in enumerate(files):
        thumb_name = fileutils.get_thumb_name(file_name, thumb_folder_path)
        imageutils.thumb(file_name, thumb_name, THUMB_SIZE)

        img = Image.open(file_name)
        exif_data = imageutils.get_exif_data(img)

        lat_lng = imageutils.get_lat_lon(exif_data)
        if not lat_lng[0] is None:
            res.append({'lat': lat_lng[0], 'lng': lat_lng[1], 'thumb': os.path.basename(thumb_name)})

        print lat_lng[0]
        print str(index + 1) + ' of ' + str(len(files))

    with open('data.txt', 'w') as outfile:
        json.dump(res, outfile)

    return res
