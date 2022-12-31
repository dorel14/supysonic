# This file is part of Supysonic.
# Supysonic is a Python implementation of the Subsonic server API.
#
# Copyright (C) 2018-2022 Alban 'spl0k' Féron
#
# Distributed under terms of the GNU AGPLv3 license.

import os.path
import shutil
import tempfile
import unittest

from supysonic.db import init_database, release_database
from supysonic.managers.folder import FolderManager
from supysonic.scanner import Scanner


class Issue101TestCase(unittest.TestCase):
    def setUp(self):
        self.__dir = tempfile.mkdtemp()
        init_database("sqlite:")
        FolderManager.add("folder", self.__dir)

    def tearDown(self):
        release_database()
        shutil.rmtree(self.__dir)

    def test_issue(self):
        firstsubdir = tempfile.mkdtemp(dir=self.__dir)
        subdir = firstsubdir
        for _ in range(4):
            subdir = tempfile.mkdtemp(dir=subdir)
        shutil.copyfile(
            "tests/assets/folder/silence.mp3", os.path.join(subdir, "silence.mp3")
        )

        scanner = Scanner()
        scanner.queue_folder("folder")
        scanner.run()

        shutil.rmtree(firstsubdir)

        scanner = Scanner()
        scanner.queue_folder("folder")
        scanner.run()


if __name__ == "__main__":
    unittest.main()
