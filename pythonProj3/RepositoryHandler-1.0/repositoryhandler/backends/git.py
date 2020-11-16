# git.py
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

import pathlib
import re

from repositoryhandler.Command import Command, CommandError
from repositoryhandler.backends import Repository,\
     RepositoryInvalidWorkingCopy, register_backend
from repositoryhandler.backends.watchers import CHECKOUT, UPDATE, \
    LOG, DIFF, BLAME, CAT, LS


def get_config(path, option=None):
    if pathlib.Path(path).is_file():
        path = pathlib.Path(path).parent

    cmd = ['git', 'config']

    if option is not None:
        cmd.extend(['--get', option])
    else:
        cmd.extend(['-l'])

    command = Command(cmd, path, env={'PAGER': ''})
    out = command.run_sync()

    if option is not None:
        return out.strip('\n\t ')

    retval = {}
    for line in out.splitlines():
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        retval[key.lower().strip()] = value.strip('\n\t ')

    if retval == {}:
        return None

    return retval


def get_repository_from_path(path) -> str:
    if pathlib.Path(path).is_file():
        path = pathlib.Path(path).parent

    dir = path
    while dir and not pathlib.Path(pathlib.Path().joinpath(dir, ".git")).is_dir() and dir != "/":
        dir = pathlib.Path(dir).parent

    if not dir or dir == "/":
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Git '
                                           'working copy' % path)
    try:
        uri = get_config(dir, 'remote.origin.url')
    except CommandError:
        uri = dir

    if uri is None or not uri:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Git '
                                           'working copy' % path)

    return 'git', uri


class GitRepository(Repository):
    '''Git Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'git')

        self.git_version = None

    def _check_uri(self, uri):
        type, repo_uri = get_repository_from_path(uri)
        if not repo_uri.startswith(self.uri):
            raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a '
                                               'Git working copy (expected %s'
                                               ' but got %s)' %
                                               (uri, self.uri, repo_uri))

    def _get_git_version(self):
        if self.git_version is not None:
            return self.git_version

        cmd = ['git', '--version']

        command = Command(cmd)
        out = command.run_sync()

        version = out.replace("git version ", "")
        self.git_version = tuple([int(i) for i in version.split('.')])

        return self.git_version

    def _get_branches(self, path):
        cmd = ['git', 'branch']

        command = Command(cmd, path)
        out = command.run_sync()

        patt = re.compile("^\*(.*)$")

        i = 0
        current = 0
        retval = []
        for line in out.splitlines():
            if line.startswith(self.uri):
                continue

            match = patt.match(line)
            if match:
                current = i
                retval.append(match.group(1).strip(' '))
            else:
                retval.append(line.strip(' '))
            i += 1

        return current, retval

    def _checkout_branch(self, path, branch):
        self._check_uri(path)

        current, branches = self._get_branches(path)

        if branch in branches:
            if branches.index(branch) == current:
                return

            cmd = ['git', 'checkout', branch]
        else:
            cmd = ['git', 'checkout', '-b', branch, 'origin/%s' % (branch)]

        command = Command(cmd, path)
        command.run()

    def __get_root_dir(self, uri) -> str:
        if uri != self.uri:
            directory = pathlib.Path(uri).parent
            while directory and not pathlib.Path(pathlib.Path().joinpath(directory,
                                                               ".git")).is_dir():
                directory = pathlib.Path(directory).parent
        else:
            directory = uri

        return directory or self.uri

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        if newdir is not None:
            srcdir = pathlib.Path().joinpath(rootdir, newdir)
        elif newdir == '.':
            srcdir = rootdir
        else:
            if module == '.':
                srcdir = pathlib.Path().joinpath(rootdir,
                                      pathlib.Path(self.uri.rstrip('/')).name())
            else:
                srcdir = pathlib.Path().joinpath(rootdir, module)
        if pathlib.Path(srcdir).exists():
            try:
                self.update(srcdir, rev)
                return
            except RepositoryInvalidWorkingCopy:
                # If srcdir is not a valid working copy,
                # continue with the checkout
                pass

        # module == '.' is a special case to download the whole repository
        if module == '.':
            uri = self.uri
        else:
            uri = pathlib.Path().joinpath(self.uri, module)

        cmd = ['git', 'clone', uri]

        if newdir is not None:
            cmd.append(newdir)
        elif module == '.':
            cmd.append(pathlib.Path(uri.rstrip('/')).name)
        else:
            cmd.append(module)

        command = Command(cmd, rootdir)
        self._run_command(command, CHECKOUT)

        if branch is not None:
            self._checkout_branch(srcdir, branch)

    def update(self, uri, rev=None):
        self._check_uri(uri)

        branch = rev
        if branch is not None:
            self._checkout_branch(uri, branch)

        cmd = ['git', 'pull']

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
        else:
            directory = uri

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def cat(self, uri, rev=None):
        self._check_uri(uri)

        cmd = ['git', 'show']

        cwd = self.__get_root_dir(uri)
        target = uri[len(cwd):].strip("/")

        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = "HEAD:%s" % (target)

        cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, CAT)

    def log(self, uri, rev=None, files=None):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
            files = [pathlib.Path(uri).parent]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
        else:
            cwd = pathlib.Path.cwd()

        cmd = ['git', 'log', '--all', '--topo-order', '--pretty=fuller',
               '--parents', '--name-status', '-M', '-C']

        # Git < 1.6.4 -> --decorate
        # Git = 1.6.4 -> broken
        # Git > 1.6.4 -> --decorate=full
        try:
            major, minor, micro = self._get_git_version()
        except ValueError:
            major, minor, micro, extra = self._get_git_version()

        if major <= 1 and minor < 6:
            cmd.append('--decorate')
        elif major <= 1 and minor == 6 and micro <= 4:
            cmd.append('--decorate')
        else:
            cmd.append('--decorate=full')

        try:
            get_config(uri, 'remote.origin.url')
            cmd.append('origin')
        except CommandError:
            pass

        if rev is not None:
            cmd.append(rev)

        if files is not None:
            for file in files:
                cmd.append(file)
        elif cwd != uri:
            cmd.append(uri)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, LOG)

    def rlog(self, module=None, rev=None, files=None):
        # Not supported by Git
        return

    def diff(self, uri, branch=None, revs=None, files=None):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = self.__get_root_dir(uri)
            files = [uri[len(cwd):].strip("/")]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
        else:
            cwd = pathlib.Path.cwd()

        cmd = ['git', 'diff']

        if revs is not None:
            if len(revs) == 1:
                cmd.append(revs[0])
            elif len(revs) > 1:
                cmd.append("{}..{}".format(revs[0], revs[1]))

        cmd.append("--")

        if files is not None:
            cmd.extend(files)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, DIFF)

    def show(self, uri, rev=None):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = self.__get_root_dir(uri)
            target = uri[len(cwd):].strip("/")
        elif pathlib.Path(uri).is_dir():
            cwd = uri
            target = None
        else:
            cwd = pathlib.Path.cwd()
            target = None

        cmd = ['git', 'show', '--pretty=format:']

        if rev is not None:
            cmd.append(rev)

        cmd.append("--")

        if target is not None:
            cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, DIFF)

    def blame(self, uri, rev=None, files=None, mc=False):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
            files = [pathlib.Path(uri).name]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
        else:
            cwd = pathlib.Path.cwd()

        cmd = ['git', 'blame', '--root', '-l', '-t', '-f']

        if mc:
            cmd.extend(['-M', '-C'])

        if rev is not None:
            cmd.append(rev)
        else:
            try:
                get_config(uri, 'remote.origin.url')
                cmd.append('origin/master')
            except CommandError:
                pass

        cmd.append('--')

        # Git doesn't support multiple files
        # we take just the first one
        cmd.append(files and files[0] or uri)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, BLAME)

    def ls(self, uri, rev=None):
        self._check_uri(uri)

        target = None
        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
            target = [pathlib.Path(uri).name]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
        else:
            cwd = pathlib.Path.cwd()

        if rev is None:
            try:
                get_config(uri, 'remote.origin.url')
                rev = 'origin/master'
            except CommandError:
                rev = 'HEAD'

        cmd = ['git',  'ls-tree', '--name-only', '--full-name', '-r', rev]

        if target is not None:
            cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, LS)

    def get_modules(self):
        #Not supported by Git
        return []

    def get_last_revision(self, uri):
        self._check_uri(uri)

        cmd = ['git', 'rev-list', 'HEAD^..HEAD']

        command = Command(cmd, uri, env={'PAGER': ''})
        try:
            out = command.run_sync()
        except:
            return None

        if out == "":
            return None

        return out.strip('\n\t ')

register_backend('git', GitRepository)
