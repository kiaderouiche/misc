# __init__.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import importlib

from repositoryhandler.backends.watchers import N_WATCHES
from repositoryhandler.Command import CommandError, CommandRunningError

DEBUG = False

__all__ = [
    'Repository',
    'RepositoryUnknownError',
    'RepositoryInvalidWorkingCopy',
    'RepositoryInvalidBranch',
    'InvalidWatch',
    'RepositoryCommandError',
    'RepositoryCommandRunningError',
    'create_repository',
    'register_backend',
    'create_repository_from_path'
]


class RepositoryUnknownError (Exception):
    '''Unkown repository type'''
    pass


class RepositoryInvalidWorkingCopy (Exception):
    '''Invalid Working Copy directory'''
    pass


class RepositoryInvalidBranch (Exception):
    '''Invalid Branch'''
    pass


class InvalidWatch (Exception):
    '''Invalid watch type'''
    pass


class RepositoryCommandError (CommandError):
    '''Error running a command'''
    pass


class RepositoryCommandRunningError (CommandRunningError):
    '''Error running a command that is still running'''
    pass


class Repository:
    '''Abstract class representing a file repository'''

    def __init__(self, uri, type):
        self.uri = uri
        self.type = type
        self.watchers = {}

    def get_uri(self) -> str:
        return self.uri

    def get_uri_for_path(self, path) -> str:
        '''Returns the repository URI corresponding to the given local path'''
        return self.uri

    def get_type(self) -> str:
        return self.type

    def copy(self):
        ''' Create a copy of the repository object.
            Watchers should not be copied'''
        raise NotImplementedError

    def checkout(self, uri, rootdir, newdir=None, branch=None, rev=None):
        '''Checkout uri to the given directory'''
        raise NotImplementedError

    def update(self, uri, rev=None):
        '''Update a working copy uri'''
        raise NotImplementedError

    def cat(self, uri, rev=None):
        '''Output the content of specified uri'''
        raise NotImplementedError

    def size(self, uri, rev=None):
        '''Output the content size of specified uri'''
        raise NotImplementedError

    def log(self, uri, rev=None, files=None):
        '''Return log for working copy uri'''
        raise NotImplementedError

    def rlog(self, module=None, rev=None, files=None):
        '''Return log directly from the repository server'''
        raise NotImplementedError

    def diff(self, uri, branch=None, revs=None, files=None):
        '''Return diff for files in working copy betweeen revisions'''
        raise NotImplementedError

    def show(self, uri, rev=None):
        '''Convenient method to get the diff for a given revision'''
        raise NotImplementedError

    def blame(self, uri, rev=None, files=None, mc=False):
        '''Return blame/annotate for files'''
        raise NotImplementedError

    def ls(self, uri, rev=None):
        '''List recursively all the files in the given uri'''
        raise NotImplementedError

    def get_modules(self):
        '''Return the list of modules of the repository'''
        raise NotImplementedError

    def get_last_revision(self, uri):
        '''Return the last revision'''
        raise NotImplementedError

    def is_ancestor(self, uri, rev1, rev2):
        '''Decide if rev1 is an ancestor of rev2'''
        raise  NotImplementedError

    def add_watch(self, type, callback, user_data=None) -> int:
        if type not in list(range(N_WATCHES)):
            raise InvalidWatch(f'Type{type} is not a valid watch type' )

        if not type in self.watchers:
            self.watchers[type] = [(callback, user_data)]
        else:
            self.watchers[type].append((callback, user_data))

        return len(self.watchers[type]) - 1

    def remove_watch(self, type, watcher_id):
        if type not in list(range(N_WATCHES)):
            raise InvalidWatch(f'Type{type} is not a valid watch type' )

        if not type in self.watchers:
            return

        try:
            self.watchers[type][watcher_id] = (None, None)
        except IndexError:
            pass
        except:
            raise

    def __run_callbacks(self, type, data):
        if not type in self.watchers:
            return

        for cb, user_data in self.watchers[type]:
            if cb is None:
                continue
            cb(data, user_data)

    def _run_command(self, command, type, input=None):
        def callback(data):
            self.__run_callbacks(type, data)

        if DEBUG:
            print((command.cmd))

        try:
            command.run(input, callback)
        except CommandError as e:
            raise RepositoryCommandError(e.cmd, e.returncode, e.error)
        except CommandRunningError as e:
            raise RepositoryCommandRunningError(e.cmd, e.error)


_backends = {}


def register_backend(backend_name, backend_class):
    _backends[backend_name] = backend_class


def _get_backend(backend_name) ->str:
    if backend_name not in _backends:
        try:
            importlib.import_module(f'repositoryhandler.backends.{backend_name}')
        except ImportError:
            pass

    if backend_name not in _backends:
        raise RepositoryUnknownError(f'Repository type {backend_name} not registered')

    return _backends[backend_name]


def create_repository(backend_name, uri) -> str:
    repo_class = _get_backend(backend_name)
    return repo_class(uri)


def create_repository_from_path(path) -> str:
    rep = None
    repo_types = ['cvs', 'svn', 'git', 'bzr', 'hg']
    for repo_type in repo_types:
        try:
            backend = 'repositoryhandler.backends.%s' % repo_type
            f = getattr(importlib.import_module(backend, None, None,
                                   ['get_repository_from_path']),
                        'get_repository_from_path')
        except ImportError:
            continue

        try:
            type, uri = f(path)
            rep = create_repository(type, uri)
            if rep is not None:
                return rep
        except:
            continue

    if rep is None:
        raise RepositoryUnknownError('Unknown repository type for path {}'.format(path))
