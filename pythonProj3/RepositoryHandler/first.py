#!/usr/bin/env  python3
#

from repositoryhandler.backends import create_repository
repo = create_repository ('cvs', ':pserver:anoncvs@anoncvs.netbsd.org:/cvs/pub/pkgsrc')
repo.checkout ('pkgsrc', '/tmp/')
