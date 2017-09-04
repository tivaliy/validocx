#
#    Copyright 2017 Vitalii Kulanov
#

import os
import yaml
import json


def safe_load(data_format, stream):
    loaders = {'json': json.load,
               'yaml': yaml.safe_load}

    if data_format not in loaders:
        raise ValueError('Unsupported data format. Only {} data formats '
                         'are allowed'.format(', '.join(loaders.keys())))

    loader = loaders[data_format]
    return loader(stream)


def safe_dump(data_format, stream, data):
    dumpers = {
        'json': lambda d, s: json.dump(data, stream, indent=4),
        'yaml': lambda d, s: yaml.safe_dump(data, stream,
                                            default_flow_style=False)
    }

    if data_format not in dumpers:
        raise ValueError('Unsupported data format. Only {} data formats '
                         'are allowed'.format(', '.join(dumpers.keys())))

    dumper = dumpers[data_format]
    dumper(data, stream)


def read_from_file(file_path):
    data_format = os.path.splitext(file_path)[1].lstrip('.')
    with open(file_path, 'r') as stream:
        return safe_load(data_format, stream)


def write_to_file(file_path, data):
    data_format = os.path.splitext(file_path)[1].lstrip('.')
    with open(file_path, 'w') as stream:
        safe_dump(data_format, stream, data)
