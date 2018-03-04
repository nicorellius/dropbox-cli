"""
dropbox-cli
Python 3 Dropbox CLI Client (API v2)

Copyright (c) 2018 Nick Vincent-Maloney <nicorellius@protonmail.com>

Mozilla Public License Version 2.0
See LICENSE in the root of the project for complete license details
"""

import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# OAuth2 access token
TOKEN = 'you need to make your own token from your account'

# CLI (`click`) options
CLICK_CONTEXT_SETTINGS = {
    'help_options': dict(help_option_names=['-h', '--help'])
}

