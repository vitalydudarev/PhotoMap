import fnmatch
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import json

EXTENSIONS = ('.jpg', '.jpeg', '.JPEG', '.JPG')
LIMIT = 30
THUMB_SIZE = 48, 48

def thumb(file_name, output_file_name, thumb_size):
    img = Image.open(file_name)
    width, height = img.size

    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(thumb_size, Image.ANTIALIAS)
    img.save(output_file_name, quality=90)

def get_files(path, extensions):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(extensions):
                files.append(os.path.join(dirpath, filename))
    return files

def get_thumb_name(file_name, thumb_path):
    basename = os.path.basename(file_name)
    name = os.path.splitext(basename)[0]
    extension = os.path.splitext(basename)[1]

    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)

    return os.path.join(thumb_path, name + '_thumb' + extension)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
        
    return None
    
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:      
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def get_photo_data(folder_path, thumb_folder_path):
    files = get_files(path, EXTENSIONS)
    create_directory(thumb_folder_path)

    res = []
    
    print 'total files: ' + str(len(files))

    for index, file_name in enumerate(files):
        thumb_name = get_thumb_name(file_name, thumb_folder_path)
        thumb(file_name, thumb_name, THUMB_SIZE)

        img = Image.open(file_name)
        exif_data = get_exif_data(img)

        lat_lng = get_lat_lon(exif_data)
        if not lat_lng[0] is None:
            res.append({'lat': lat_lng[0], 'lng': lat_lng[1], 'thumb': os.path.basename(thumb_name)})

        print lat_lng[0]
        print str(index + 1) + ' of ' + str(len(files))

    with open('data.txt', 'w') as outfile:
        json.dump(res, outfile)

    return res
