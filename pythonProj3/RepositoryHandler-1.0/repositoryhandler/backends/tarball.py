# tarball.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
# Copyright (C) 2007 GSyC/LibreSoft Group
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

from repositoryhandler.Command import Command
from repositoryhandler.backends import Repository, register_backend
from repositoryhandler.backends.watchers import CHECKOUT
from repositoryhandler.Downloader import get_download_command

### FileExtractor
import tarfile
import zipfile
import gzip
import bz2


def is_gzipfile(uri):
    try:
        import gzip
        t = gzip.GzipFile(uri, "r")
        t.close()
        return True
    except:
        return False


def is_bz2file(uri):
    try:
        import bz2
        t = bz2.BZ2File(uri, "r")
        t.close()
        return True
    except:
        return False


class FileExtractorError(Exception):
    """
    Raised if an error occurs during the extraction process
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


class FileExtractor:

    def __init__(self, uri):
        self.uri = uri

    def extract(self, path=None):
        raise NotImplementedError


class TarFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            tar = tarfile.open(self.uri, 'r:*')
        except tarfile.TarError as e:
            raise FileExtractorError("FileExtractor Error: Opening tarfile "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = pathlib.Path.cwd()

        try:
            tar.extractall(path)
        except tarfile.TarError as e:
            tar.close()
            raise FileExtractorError(f"FileExtractor Error: Extracting tarfile {self.uri}: {str(e)}")

        tar.close()


class ZipFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            zip = zipfile.ZipFile(self.uri, 'r')
        except zipfile.BadZipfile as e:
            raise FileExtractorError("FileExtractor Error: Opening zipfile"
                                     " %s: %s" % (self.uri, str(e)))

        if path is None:
            path = pathlib.Path.cwd()

        for name in zip.namelist():
            try:
                fpath = pathlib.Path().joinpath(path, name)

                # Check if 'name' is a directory
                if name[-1] == '/':
                    try:
                        pathlib.Path(fpath).mkdir(parents=True, exist_ok=True)                       
                    except IOError as e:
                        zip.close()
                        raise FileExtractorError("FileExtractor Error: Write "
                                                 "error while extracting "
                                                 "zipfile %s: %s" %
                                                 (self.uri, str(e)))
                else:
                    bytes = zip.read(name)

                    f = open(fpath, 'w')
                    try:
                        f.write(bytes)
                    except IOError as e:
                        zip.close()
                        f.close()
                        raise FileExtractorError("FileExtractor Error: Write "
                                                 "error while extracting "
                                                 "zipfile %s: %s" %
                                                 (self.uri, str(e)))
                    f.close()
            except zipfile.BadZipfile as e:
                zip.close()
                raise FileExtractorError("FileExtractor Error: Reading "
                                         "zipfile %s: %s" % (self.uri, str(e)))
        zip.close()


class GzipFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            gz = gzip.GzipFile(self.uri, 'r')
        except Exception as e:
            raise FileExtractorError("FileExtractor Error: Opening gzip "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = pathlib.Path.cwd()

        try:
            path = pathlib.Path().joinpath(path,
                                self.uri.split("/")[-1].replace(".gz", ""))
            with open(path, "w") as f:
                f.write(gz.read())
        except Exception as e:
            gz.close()
            raise FileExtractorError("FileExtractor Error: Extracting gzip "
                                     "%s: %s" % (self.uri, str(e)))
        finally:
            f.close()

        gz.close()


class Bzip2FileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            file_bz2 = bz2.BZ2File(self.uri, 'r')
        except Exception as e:
            raise FileExtractorError("FileExtractor Error: Opening bzip2 "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = pathlib.Path.cwd()

        try:
            path = pathlib.Path().joinpath(path,
                                self.uri.split("/")[-1].replace(".bz2", ""))
            with open(path, 'w') as f:
                f.write(file_bz2.read())
        except Exception as e:
           file_bz2.close()
           raise FileExtractorError("FileExtractor Error: Extracting bzip2"
                                     " %s: %s" % (self.uri, str(e)))
        finally:
            f.close()
        file_bz2.close()


def create_file_extractor(uri):
    if tarfile.is_tarfile(uri):
        return TarFileExtractor(uri)
    elif zipfile.is_zipfile(uri):
        return ZipFileExtractor(uri)
    elif is_gzipfile(uri):
        return GzipFileExtractor(uri)
    elif is_bz2file(uri):
        return Bzip2FileExtractor(uri)

    raise FileExtractorError("FileExtractor Error: URI '%s' doesn't look like "
                             "a valid tarball or compressed file" % (uri))


class TarballRepository(Repository):
    '''Tarball Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'tarball')

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        if newdir is not None:
            srcdir = pathlib.Path().joinpath(rootdir, newdir)
        else:
            srcdir = rootdir
        if not pathlib.Path(srcdir).exists():
            pathlib.Path(srcdir).mkdir(parents=True, exist_ok=True)

        if pathlib.Path(module).exists():
            tarball_path = module
        else:
            # Download module to rootdir
            filename = pathlib.Path(module).name.split('?')[0]
            tarball_path = pathlib.Path().joinpath(srcdir, filename)
            cmd = get_download_command(module, tarball_path, '/dev/stdout')
            if cmd is None:
                return

            command = Command(cmd, srcdir)
            self._run_command(command, CHECKOUT)

            if not pathlib.Path(tarball_path).exists():
                return

        # Unpack the tarball
        fe = create_file_extractor(tarball_path)
        fe.extract(srcdir)

register_backend('tarball', TarballRepository)
