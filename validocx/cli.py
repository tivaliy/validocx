#
#    Copyright 2017 Vitalii Kulanov
#

import argparse
import json
import os
import sys

from docx import Document

from validocx.extractor import extract


def _get_file_path(file_path):
    if not os.path.lexists(file_path):
        raise argparse.ArgumentTypeError(
            "File '{0}' does not exist".format(file_path))
    return file_path


def create_parser():
    parser = argparse.ArgumentParser(description='docx-file validation CLI.')
    parser.add_argument(
        '-f', '--file',
        required=True,
        type=_get_file_path,
        help='docx format file to be validated.'
    )
    parser.add_argument(
        '-s', '--style',
        required=True,
        nargs='+',
        help='Styles to be fetched and analyzed.'
    )
    return parser


def parse_args(args):
    parser = create_parser()
    parsed_args = vars(parser.parse_args(args=args))
    return parsed_args


def main(args=sys.argv[1:]):
    sys.exit(run(arguments=parse_args(args=args)))


def run(arguments, stdout=sys.stdout):
    document = Document(docx=arguments['file'])
    data = extract(document, styles=arguments['style'])
    stdout.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
