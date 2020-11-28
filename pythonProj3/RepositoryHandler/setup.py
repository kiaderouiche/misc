#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 GSyC/LibreSoft, Universidad Rey Juan Carlos
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
#
# Allow for environments without setuptools
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup  # pylint: disable=ungrouped-imports

from distutils.core import Extension
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsPlatformError, DistutilsExecError

setup(name="RepositoryHandler",
      version="1.0.0",
      author="GSyC/LibreSoft, Universidad Rey Juan Carlos",
      author_email="metrics-grimoire@lists.libresoft.es",
      description="Python library for handling code repositories",
      url="http://github.com/MetricsGrimoire/RepositoryHandler",
      packages=['repositoryhandler', 'repositoryhandler.backends'],
      python_requires='>=3.8',
)
