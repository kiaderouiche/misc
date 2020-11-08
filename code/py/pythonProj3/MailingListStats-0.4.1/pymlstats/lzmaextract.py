#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:49:23 2020

@author: jihbed
"""

import lzma

with open('./accountsservice-0.6.42.tar.xz', encoding="utf8", errors='ignore') as compressed:
    with lzma.LZMAFile(compressed) as uncompressed:
        for line in uncompressed:
            print(line, encoding = 'unicode_escape')