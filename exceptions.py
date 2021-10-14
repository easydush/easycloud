class NoSuchAlbumException(Exception):
    def __str__(self):
        return 'No such album.'


class NoSuchPathException(Exception):
    def __str__(self):
        return 'No such path.'


class NoArgumentsException(Exception):
    def __str__(self):
        return 'Path and album are required.'


class NoDataException(Exception):
    def __str__(self):
        return 'No data.'


class IncorrectFileException(Exception):
    def __str__(self):
        return 'That file is not photo.'
