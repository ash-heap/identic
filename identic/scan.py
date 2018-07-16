import sys
import os
import hashlib
from collections import OrderedDict


def blocks(file, blocksize=65536):
    with open(file, 'rb') as f:
        block = f.read(blocksize)
        while len(block) > 0:
            yield block
            block = f.read(blocksize)


def checksum(file, hash):
    hash = hash()
    for block in blocks(file):
        hash.update(block)
    return hash.digest()


def count_files(top, follow_links=False, progress=False):
    num_files = 0
    if progress:
        from progressbar import (
            ProgressBar, UnknownLength,
            AnimatedMarker, BouncingBar, Counter, Timer)
        widgets = [
            AnimatedMarker(), ' ',
            Counter('%(value)d files found'), ' ',
            BouncingBar(), ' ',
            Timer()]
        with ProgressBar(max_value=UnknownLength, widgets=widgets) as progress:
            for _, _, files in os.walk(top, followlinks=follow_links):
                num_files = num_files + len(files)
                progress.update(num_files)
    else:
        for _, _, files in os.walk(top, followlinks=follow_links):
            num_files = num_files + len(files)
    return num_files


def handle_walk_error(err):
    errstr = '\n{:s}: {:s}'.format(err.strerror, err.filename)
    print(errstr, file=sys.stderr)


def scan_dir(top, hash=hashlib.sha256, follow_links=False, progress=False):
    num_files = count_files(top, follow_links=follow_links, progress=progress)
    if progress:
        from progressbar import (
            ProgressBar, UnknownLength, Percentage, ETA, Bar, SimpleProgress,
            AnimatedMarker, BouncingBar, Counter, Timer)
        widgets = [
            Percentage(), ' (',
            SimpleProgress('scanning file %(value_s)s of %(max_value_s)s'),
            ') ', Bar(), ' ', Timer(), ' ', ETA()]
        with ProgressBar(max_value=num_files, widgets=widgets) as progress:
            return _scan_dir(top, hash, follow_links, progress.update)
    else:
        def nop(x):
            pass
        return _scan_dir(top, hash, follow_links, nop)

def _scan_dir(top, hash, follow_links, update):
    count = 0
    file_checksums = OrderedDict()
    for root, dirs, files in os.walk(
            top, followlinks=follow_links, onerror=handle_walk_error):
        dirs.sort()
        files.sort()
        for file in files:
            count = count + 1
            update(count)
            try:
                fullpath = os.path.join(root, file)
                file_checksums.setdefault(
                    checksum(fullpath, hash).hex(), []).append(fullpath)
            except (FileNotFoundError, PermissionError, OSError) as err:
                errstr = '\n{:s}: {:s}'.format(err.strerror, err.filename)
                print(errstr, file=sys.stderr)
    return file_checksums

