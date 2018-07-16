import sys
import json
from identic.options import get_options
from identic.scan import scan_dir
from identic.io import save_file, load_file
from identic.report import print_report


def main():
    options = get_options(sys.argv[1:])
    if options.infile:
        hashes = load_file(options.infile)
    else:
        hashes = scan_dir(
            options.dir,
            hash=options.hash,
            follow_links=options.follow_links,
            progress=options.progress)
        if options.outfile:
            save_file(options.outfile, hashes)
    if options.report:
        print_report(hashes, duplicates_only=options.duplicates_only)
