#
#    Copyright 2017 Vitalii Kulanov
#

import argparse
import os
import sys

from docx import Document

from validocx import utils
from validocx.validator import validate


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
        help='Docx file to be validated.'
    )
    parser.add_argument(
        '-r', '--requirements',
        required='True',
        type=_get_file_path,
        help='File with the requirements. In YAML or JSON format.'
    )
    return parser


def parse_args(args):
    parser = create_parser()
    parsed_args = vars(parser.parse_args(args=args))
    return parsed_args


def run(arguments, stdout=sys.stdout):
    document = Document(docx=arguments['file'])
    schema = utils.read_from_file(arguments['requirements'])
    validate(document, schema)
    stdout.write("Validation process completed successfully.\n")


def main(args=sys.argv[1:]):
    sys.exit(run(arguments=parse_args(args=args)))


if __name__ == '__main__':
    main()
