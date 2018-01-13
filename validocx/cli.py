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


class MessageCounterHandler(logging.Handler):
    msg_level_count = None

    def __init__(self, *args, **kwargs):
        super(MessageCounterHandler, self).__init__(*args, **kwargs)
        self.msg_level_count = {}

    def emit(self, record):
        level = record.levelname
        if level not in self.msg_level_count:
            self.msg_level_count[level] = 0
        self.msg_level_count[level] += 1


def _get_file_path(file_path):
    if not os.path.lexists(file_path):
        raise argparse.ArgumentTypeError(
            "File '{0}' does not exist".format(file_path))
    return file_path


def create_parser():
    parser = argparse.ArgumentParser(description='docx-file validation CLI.')
    parser.add_argument(
        'docx-file',
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
    logging.basicConfig(level=level, format=CONSOLE_LOG_FORMAT)
    root_logger = logging.getLogger()
    mch = MessageCounterHandler()
    root_logger.addHandler(mch)
    if log_file:
        fh = logging.FileHandler(filename=log_file)
        fh.setLevel(level=level)
        formatter = logging.Formatter(fmt=FILE_LOG_FORMAT, datefmt=DATE_FORMAT)
        fh.setFormatter(formatter)
        root_logger.addHandler(fh)

    requirements = utils.read_from_file(arguments['requirements'])
    validate(arguments['docx-file'], requirements)
    root_logger.info("Summary results: Errors - {0}, "
                     "Warnings - {1}".format(mch.msg_level_count['ERROR'],
                                             mch.msg_level_count['WARNING']))


def main(args=sys.argv[1:]):  # pragma: no cover
    sys.exit(run(arguments=parse_args(args=args)))
