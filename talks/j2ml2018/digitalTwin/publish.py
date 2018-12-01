#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys


def _run():
	subprocess.call('jupyter nbconvert slides.ipynb --to slides --post serve --ServePostProcessor.reveal_cdn="http://cdn.jsdelivr.net/reveal.js/2.5.0"', shell=True)

def _help():
	print("jupyter launcher")

def _version():
	print("1.0.0")

def main():
	parser = argparse.ArgumentParser(description="jupyter launcher")

	parser.add_argument('ipynb files', nargs='?')
	parser.add_argument('-r', '--run', type=str, default="", help="launcher jupyter presentation")
	parser.add_argument('-a', '--about', action='store_true', default=False, help="A propos du logiciel")
	parser.add_argument('-v', '--version', action='store_true', default=False, help="Version du logiciel")

	dargs = vars(parser.parse_args())

	if dargs['about']:
		_help()
		sys.exit()
	if dargs['version']:
		_version()
		sys.exit()
	if dargs['run']:
		_run()
		sys.exit()

if __name__ == '__main__':
	main()