#!/usr/bin/env python3

import pathlib
from repositoryhandler.backends import create_repository
from tests import Test, register_test, remove_directory


class TarballTest (Test):

    def checkout(self):
        # checkout
        self.repo = create_repository('tarball', None)
        self.repo.checkout(
            'https://www.cairographics.org/snapshots/pycairo-1.1.6.tar.gz', '/tmp/')
        if not pathlib.Path('/tmp/pycairo-1.1.6.tar.gz').exists():
            print ("Tarball checkout: FAILED")
            return
        elif not pathlib.Path('/tmp/pycairo-1.1.6/ChangeLog').exists():
            print ("Tarball checkout: FAILED")
            return

        # checkout with local path
        self.repo.checkout('/tmp/pycairo-1.1.6.tar.gz', '/tmp/pycairo-local')
        if not pathlib.Path('/tmp/pycairo-local/pycairo-0.4.0/ChangeLog').exists():
            print ("Tarball checkout: FAILED")
            return

        # Mbox
        self.repo.checkout('http://lists.morfeo-project.org/pipermail/'
                           'libresoft-tools-devel/2007-April.txt.gz',
                           '/tmp')
        if not pathlib.Path('/tmp/2007-April.txt').exists():
            print ("Tarball checkout: FAILED")
            return

        print ("Tarball checkout: FAILED")

        # TODO: check zip

    def clean(self):
        pathlib.Path.unlink('/tmp/pycairo-1.1.6.tar.gz')
        remove_directory('/tmp/pycairo-1.1.6/')
        remove_directory('/tmp/pycairo-local')
        pathlib.Path.unlink('/tmp/2007-April.txt')

register_test('tarball', TarballTest)
