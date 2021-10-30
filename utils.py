import os

PHOTO_EXTENSIONS = ['.jpg', '.jpeg']
FACE_PREFIX = '/faces/'


def correct_extension(path):
    return any([extension in path for extension in PHOTO_EXTENSIONS])


def unchecked_photo(path):
    return correct_extension(path) and (FACE_PREFIX not in path)


def is_dir(path):
    return os.path.isdir(path)
