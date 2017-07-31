import fnmatch
import os


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
