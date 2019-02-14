# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2019

import sys

import codecs
import fnmatch

from unidiff import PatchSet
from arghandler import ArgumentHandler, subcmd

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


@subcmd('rm', help='Remove a file from the diff')
def cmd_rm(handler, context, args):
    handler.add_argument('filename', nargs="+")
    args = handler.parse_args(args)

    for patchfile in context['patch']:
        matches = False
        for pattern in args.filename:
            if fnmatch.fnmatch(patchfile.path, pattern):
                matches = True
                break

        if not matches:
            sys.stdout.write(unicode(patchfile))


@subcmd('filterout', help='Filter out different kinds of files')
def cmd_filterout(handler, context, args):
    handler.add_argument('-f', '--files', action='append', default=[], nargs='?',
                         help="Filter files. Use -fr, -fa")
    handler.add_argument('-l', '--lines', action='append', default=[], nargs='?',
                         help="Filter lines. Use -lr, -la, -lc")

    args = handler.parse_args(args)

    args.files = set(args.files)
    args.lines = set(args.lines)

    if None in args.files:
        args.files = set(['r'])
    if None in args.lines:
        args.lines = set(['r'])

    rmfiles = []

    for patchidx, patchfile in enumerate(context['patch']):
        if ("r" in args.files and patchfile.is_removed_file) or \
           ("a" in args.files and patchfile.is_added_file):
            rmfiles.append(patchidx)
        else:
            for hunk in patchfile:
                rmlines = []
                for lineidx, line in enumerate(hunk):
                    if ("a" in args.lines and line.is_added) or \
                       ("r" in args.lines and line.is_removed) or \
                       ("c" in args.lines and line.is_context):
                        rmlines.append(lineidx)
                for lineidx in reversed(rmlines):
                    # https://github.com/matiasb/python-unidiff/issues/58
                    if hunk[lineidx].is_added:
                        hunk.added -= 1
                        hunk.target_length -= 1
                    if hunk[lineidx].is_removed:
                        hunk.removed -= 1
                        hunk.source_length -= 1

                    hunk.pop(lineidx)

    for fileidx in reversed(rmfiles):
        context['patch'].pop(fileidx)

    sys.stdout.write(unicode(context['patch']))


def main():
    def load_context(args):
        if args.input == sys.stdin:
            data = codecs.getreader('utf8')(sys.stdin).read()
        else:
            data = codecs.open(args.input, encoding="utf-8").read()
        return {
            "gargs": args,
            "patch": PatchSet(data)
        }

    handler = ArgumentHandler()
    handler.add_argument('-f', '--file', default=sys.stdin, dest='input',
                         help="The file to input from")

    try:
        handler.run(sys.argv[1:], context_fxn=load_context)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
