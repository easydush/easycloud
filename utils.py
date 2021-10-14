import os

PHOTO_EXTENSIONS = ['.jpg', '.jpeg']


def correct_extension(path):
    return any([extension in path for extension in PHOTO_EXTENSIONS])


def is_dir(path):
    return os.path.isdir(path)
