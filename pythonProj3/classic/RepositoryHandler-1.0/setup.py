#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 GSyC/LibreSoft, Universidad Rey Juan Carlos
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
try:
    from setuptools import setup
except:
    from distutils.core import setup

#Ajouter le support pour Python3.7, 3.8+
#Ajouter le support pour Wget, et surtout py-httpie
#Ajouter un prefix pour NetBSD
#Ajouter le support pour les programmes, pygit, pybzr, pycvs et pysvn,  et etc
setup(name="RepositoryHandler",
      version="1.0", #Total Support Python3.7, Python.8
      author="GSyC/LibreSoft, Universidad Rey Juan Carlos",
      author_email="libresoft-tools-devel@lists.morfeo-project.org",
      description="Python library for handling code repositories",
      url="http://metricsgrimoire.github.io/RepositoryHandler/",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
     ],
      packages=['repositoryhandler', 'repositoryhandler.backends']
)
