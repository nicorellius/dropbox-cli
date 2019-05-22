#!/usr/bin/env python

"""
dropbox-cli
Python 3 Dropbox CLI Client (API v2)

Copyright (c) 2018 Nick Vincent-Maloney <nicorellius@protonmail.com>

Mozilla Public License Version 2.0
See LICENSE in the root of the project for complete license details
"""

import logging
import contextlib
import datetime
import os
import time
import json

from pprint import pprint

import click

from dropbox import Dropbox, exceptions, files

import config

from utils import print_json


API_TOKEN = '' # Edit your own Token


logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)


# 'Click' is Python tool for making clean CLIs
@click.command(context_settings=config.CLICK_CONTEXT_SETTINGS['help_options'])
@click.argument('api_token', required=True)
@click.option('-l', '--list-files', help='List files in your Dropbox',
              type=click.Path())
@click.option('-d', '--download', help='Download a file from your Dropbox',
              type=click.File())
@click.option('-u', '--upload', help='Upload a file to your Dropbox',
              type=click.File())
@click.option('-p', '--path', help='For upload option, path to file',
              type=click.Path())
@click.option('-o', '--overwrite', help='For upload option, overwrite file?',
              type=click.BOOL)
def main(api_token: str,
         download: str,
         upload: str, path: str, overwrite: bool = False,
         list_files: str = ''):

    dbx = Dropbox(api_token)
    logging.info(f'Thanks for entering your API token {dbx}')

    _list_files(dbx, list_files)
    _upload(dbx, upload, path, overwrite)


def _list_files(dbx, path):

    """
    List files im a folder.
    """

    try:
        with _stopwatch('list_folder'):
            res = dbx.files_list_folder(path)

    except exceptions.ApiError as err:

        print('Folder listing failed for', path, '-- assumed empty:', err)

        return {}

    else:
        rv = {}

        for entry in res.entries:
            rv[entry.name] = entry

    # print([x for x in rv])

    for x in rv:
        print(f'  - {x}')
        # for y in rv[x]:
        #     print(y, ':', rv[x][y])


def _download(dbx, folder, subfolder, name):

    """
    Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """

    path = '{0}{1}{2}'.format(folder,
                              subfolder.replace(os.path.sep, '/'),
                              name)

    while '//' in path:
        path = path.replace('//', '/')

    with _stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except exceptions.HttpError as err:
            print('*** HTTP error', err)

            return None

    data = res.content

    print(len(data), 'bytes; md:', md)

    return data


def _upload(dbx, filename, path, overwrite=False):

    """
    Upload a file.
    Return the request response, or None in case of error.
    """

    if overwrite:
        mode = files.WriteMode.overwrite
    else:
        mode = files.WriteMode.add

    mtime = os.path.getmtime(filename)

    with open(filename, 'rb') as f:
        data = f.read()

    with _stopwatch('Upload {0} bytes'.format(len(data))):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except exceptions.ApiError as err:
            print('*** API error', err)

            return None

    logging.info('Uploaded as {0}'.format(res.name.encode('utf8')))

    return res


@contextlib.contextmanager
def _stopwatch(message):
    """
    Context manager to print how long a block of code took.
    """

    t0 = time.time()

    try:
        yield

    finally:
        t1 = time.time()
        logging.info('Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    main()
