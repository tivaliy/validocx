#
#    Copyright 2017 Vitalii Kulanov
#

import argparse
import logging
import os
import sys

from . import utils
from .validator import validate

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CONSOLE_LOG_FORMAT = '%(levelname)s: %(message)s'
FILE_LOG_FORMAT = ('%(asctime)s.%(msecs)03d %(levelname)s '
                   '(%(module)s) %(message)s')


def configure_logging(level, file_path=None):
    logging.basicConfig(level=level, format=CONSOLE_LOG_FORMAT)
    if file_path:
        fh = logging.FileHandler(filename=file_path)
        fh.setLevel(level=level)
        formatter = logging.Formatter(fmt=FILE_LOG_FORMAT, datefmt=DATE_FORMAT)
        fh.setFormatter(formatter)
        logging.getLogger().addHandler(fh)


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
        required=True,
        type=_get_file_path,
        help='File with the requirements. In YAML or JSON format.'
    )
    parser.add_argument(
        '--log-file',
        help='Log file to store logs.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-q', '--quiet',
        dest='level',
        action='store_const',
        const='quite',
        help='Decrease output verbosity.'
    )
    group.add_argument(
        '-v', '--verbose',
        dest='level',
        action='store_const',
        const='verbose',
        help='Increase output verbosity.'
    )
    return parser


def parse_args(args):
    parser = create_parser()
    parsed_args = vars(parser.parse_args(args=args))
    return parsed_args


def run(arguments):
    log_map = {'quite': logging.ERROR,
               'verbose': logging.DEBUG}
    level = log_map[arguments['level']] if arguments['level'] else logging.INFO
    log_file = arguments['log_file'] if arguments['log_file'] else None
    configure_logging(level=level, file_path=log_file)

    requirements = utils.read_from_file(arguments['requirements'])
    validate(arguments['file'], requirements)


def main(args=sys.argv[1:]):
    sys.exit(run(arguments=parse_args(args=args)))
