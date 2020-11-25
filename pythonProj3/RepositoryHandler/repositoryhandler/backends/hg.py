# git.py
#
# Copyright (C) 2020 K.I.A.Derouiche <kamel.derouiche@gmail.com>
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
    RepositoryInvalidWorkingCopy, register_backend, RepositoryCommandError
from repositoryhandler.backends.watchers import BLAME, LOG, DIFF, \
            LS, CAT, UPDATE, SIZE, CHECKOUT


def get_config(path, option=None) -> int:
    if pathlib.Path(path).is_file():
        path = pathlib.Path(path).parent

    cmd = ['hg', 'config']

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
        raise RepositoryInvalidWorkingCopy('"{}" does not appear to be a Git '
                                           'working copy'.format(path))
    try:
        uri = get_config(dir, 'remote.origin.url')
    except CommandError:
        uri = dir

    if uri is None or not uri:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Git '
                                           'working copy' % path)

    return 'git', uri


class HgRepository(Repository):
    '''Hg Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'hg')

        self.git_version = None

    def _check_uri(self, uri):
        type, repo_uri = get_repository_from_path(uri)
        if not repo_uri.startswith(self.uri):
            raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a '
                                               'Git working copy (expected %s'
                                               ' but got %s)' %
                                               (uri, self.uri, repo_uri))

    def _get_git_version(self)-> str:
        if self.git_version is not None:
            return self.git_version

        cmd = ['hg', '--version']

        command = Command(cmd)
        out = command.run_sync()
        # it could looks like:
        #  hg version 1.7.10.4 // 1.8.4.rc3 // 1.7.12.4 (Apple Git-37) // 1.9.3 (Apple Git-50)

        version = out.replace("hg version ", "")
        try:
            self.git_version = tuple([int(i) for i in version.split('.')])
        except ValueError:
            self.git_version = tuple([int(i) for i in version.split()[0].split('.')[0:3]])

        return self.git_version

    def _get_branches(self, path) -> str:
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

    def __get_root_dir(self, uri)-> str:
        if uri != self.uri:
            directory = pathlib.Path(uri).parent
            while directory and not pathlib.Path(pathlib.Path().joinpath(directory,
                                                               ".git")).is_dir():
                directory = pathlib.Path(directory).parent
        else:
            directory = uri

        return directory or self.uri

    def copy(self) -> str:
        repo = HgRepository(self.uri)
        repo.git_version = self.git_version
        return repo

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

        cmd = ['hg', 'clone', uri]

        if newdir is not None:
            cmd.append(newdir)
        elif module == '.':
            cmd.append(pathlib.Path(uri.rstrip('/')).name)
        else:
            cmd.append(module)

        def ignore_progress_stderr(*args):
            return True

        command = Command(cmd, rootdir,
                          error_handler_func=ignore_progress_stderr)
        self._run_command(command, CHECKOUT)

        if branch is not None:
            self._checkout_branch(srcdir, branch)

    def update(self, uri, rev=None):
        self._check_uri(uri)

        branch = rev
        if branch is not None:
            self._checkout_branch(uri, branch)

        cmd = ['hg', 'pull']

        if pathlib.Path(uri).is_file():
            directory = pathlib.Path(uri).parent
        else:
            directory = uri

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def cat(self, uri, rev=None):
        self._check_uri(uri)

        cmd = ['hg', 'show']

        cwd = self.__get_root_dir(uri)
        target = uri[len(cwd):].strip("/")

        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = "HEAD:%s" % (target)

        cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, CAT)

    def size(self, uri, rev=None):
        self._check_uri(uri)

        cmd = ['hg', 'cat-file', '-s']

        cwd = self.__get_root_dir(uri)
        target = uri[len(cwd):].strip("/")

        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = "HEAD:%s" % (target)

        cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, SIZE)

    def log(self, uri, rev=None, files=None, gitref=None):
        self._check_uri(uri)

        if pathlib.Path(uri).is_file():
            cwd = pathlib.Path(uri).parent
            files = [pathlib.Path(uri).name]
        elif pathlib.Path(uri).is_dir():
            cwd = uri
        else:
            cwd = pathlib.Path.cwd()

        cmd = ['hg', 'log', '--topo-order', '--pretty=fuller',
               '--parents', '--name-status', '-M', '-C', '-c']

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


        if gitref:
            cmd.append(gitref)
        else:
            try:
                get_config(uri, 'remote.origin.url')

                if major <= 1 and minor < 8:
                    cmd.append('origin')
                else:
                    cmd.append('--remotes=origin')
            except CommandError:
                pass
            cmd.append('--all')

        if rev is not None:
            cmd.append(rev)

        if files:
            cmd.append('--')
            for file in files:
                cmd.append(file)
        elif cwd != uri:
            cmd.append(uri)

        command = Command(cmd, cwd, env={'PAGER': ''})
        try:
            self._run_command(command, LOG)
        except RepositoryCommandError:
            pass

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

        cmd = ['hg', 'diff']

        if revs is not None:
            if len(revs) == 1:
                cmd.append(revs[0])
            elif len(revs) > 1:
                cmd.append("%s..%s" % (revs[0], revs[1]))

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

        cmd = ['hg', 'show', '--pretty=format:']

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

        cmd = ['hg', 'blame', '--root', '-l', '-t', '-f']

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
            target = pathlib.Path(uri).name
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

    def get_modules(self)-> list:
        #Not supported by Git
        return []

    def get_last_revision(self, uri)-> str:
        self._check_uri(uri)

        cmd = ['hg', 'rev-list', 'HEAD^..HEAD']

        command = Command(cmd, uri, env={'PAGER': ''})
        try:
            out = command.run_sync()
        except:
            return None

        if out == "":
            return None

        return out.strip('\n\t ')

    def is_ancestor(self, uri, rev1, rev2):
        self._check_uri(uri)
        version = self._get_git_version()

        if version[0] == 0 or (version[0] == 1 and version[1] < 8):
            # Should we implement an workaround for git under 1.8 or
            # just have git 1.8 or later in prerequisites?
            # An workaround can be found at
            # http://stackoverflow.com/a/3006203/1305362
            raise NotImplementedError

        # 'git merge-base --is-ancestor' is only supported after 1.8
        cmd = ['hg', 'merge-base', '--is-ancestor', rev1, rev2]
        command = Command(cmd, uri, env={'PAGER': ''})
        try:
            command.run()
            return True
        except CommandError as e:
            if e.returncode == 1:
                return False
            else:
                raise e


register_backend('hg', HgRepository)
