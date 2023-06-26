import sys
import os


def get_platform():  # pragma: no cover
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]


def get_files(des_dir):
    files = [os.path.basename(f) for f in os.listdir(des_dir) if os.path.isfile(os.path.join(des_dir, f))]
    return files
