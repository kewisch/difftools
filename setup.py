# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2015

import os
from setuptools import setup

setup(
    name = "difftools",
    version = "1.0.0",
    author = "Philipp Kewisch",
    author_email = "mozilla@kewis.ch",
    description = ("Tools to modify patch files for easier review"),
    license = "MPL-2.0",
    keywords = "diff patch",
    url = "https://github.com/kewisch/difftools",
    packages = ['difftools'],
    install_requires = [
        'arghandler >=1.0.3',
        'unidiff'
    ],
    entry_points = {
        'console_scripts': ['difftools=difftools.cli:main']
    },
    classifiers = [
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
    ]
)
