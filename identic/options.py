import sys
import argparse
import hashlib


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

def formatter(prog):
    return CustomHelpFormatter(prog, max_help_position=30)


def make_parser():
    parser = argparse.ArgumentParser(
        formatter_class=formatter,
        description="""Find and report duplicate files.
""")
    parser.add_argument(
        'dir', metavar='DIR', nargs='?',
        help='directory to look for duplicate files under')
    parser.add_argument(
        '-o', '--out-file', dest='outfile',
        help='save results to a JSON format file for later use')
    parser.add_argument(
        '-l', '--follow-links', dest='follow_links', action='store_true',
        help='follow symbolic links, this can lead to infinite recursion')
    parser.add_argument(
        '-p', '--progress', dest='progress', action='store_true',
        help='print progress to stderr')
    parser.add_argument(
        '-f', '--in-file', dest='infile',
        help='load results from a JSON format file saved earlier')
    parser.add_argument(
        '-r', '--report', dest='report', action='store_true',
        help='print report of duplicate files')
    parser.add_argument(
        '-d', '--duplicates-only', dest='duplicates_only', action='store_true',
        help='only report duplicate files')
    parser.add_argument(
        '-c', '--hash', dest='hash', type=str, default='SHA256',
        help='hashing algorithm, MD5, SHA1, (SHA256 default), SHA512')
    return parser

def get_options(argv):
    parser = make_parser()
    options = parser.parse_args(argv)
    # verify directory input
    if not options.dir and not options.infile:
        print(parser.format_usage().rstrip(), file=sys.stderr)
        print('DIR required if --in-file is not given', file=sys.stderr)
        sys.exit(1)
    # parse hash string to hash function
    if options.hash.upper() == 'MD5':
        options.hash = hashlib.md5
    elif options.hash.upper() == 'SHA1':
        options.hash = hashlib.sha1
    elif options.hash.upper() == 'SHA256':
        options.hash = hashlib.sha256
    elif options.hash.upper() == 'SHA512':
        options.hash = hashlib.sha512
    return options
