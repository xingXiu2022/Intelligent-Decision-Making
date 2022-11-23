"""
A tool to parse xmind file into programmable data types.
Check https://github.com/chencanxin/xmind2json to see supported types.

Usage:
 xmind2json [path_to_xmind_file] -[type]

Example:
 xmind2json C:\\tests\\my.xmind -json
 xmind2json C:\\tests\\my.xmind -xml

"""

import sys

from xmind2json import *


def main():
    if len(sys.argv) >= 2 and sys.argv[1].endswith('.xmind'):
        xmind = sys.argv[1]
        out_types = 'json'
        if len(sys.argv) >= 3:
            out_types = sys.argv[2][1:]

        out = xmind_to_file(xmind, out_types)
        print('Generated: {}'.format(out))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
