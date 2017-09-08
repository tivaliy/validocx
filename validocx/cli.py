#
#    Copyright 2017 Vitalii Kulanov
#

import argparse
import logging
import os
import sys

from . import utils
from .validator import validate

logging.basicConfig(
    format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


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


def run(arguments):
    requirements = utils.read_from_file(arguments['requirements'])
    validate(arguments['file'], requirements)
    logger.info("Validation process completed successfully.\n")


def main(args=sys.argv[1:]):
    sys.exit(run(arguments=parse_args(args=args)))
