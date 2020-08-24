#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

def rmdir(dir):
	dir = Path(dir)
	print("==>", dir)
	for item in dir.iterdir():
		print("Acte0: {}".format(item))
		if item.is_dir():
			print('Acte1:directory... {}'.format(item))
			yield rmdir(item)
		else:
			print('Acte2:suppr... {}'.format(item))
			yield item.unlink()
	dir.rmdir()

# class dirrmdir:
# 	def __init__(self, dir):
# 		self.dir = Path(dir)

# 	def rmdir(self):
# 		for item in self.dir.iterdir():
# 			if item.is_dir():
# 				self.rmdir(item)
# 			else:
# 				item.unlink()
# 		self.dir.self.rmdir()

def main():
	# directory = dirrmdir("/home/jihbed/researchAct/")
	# directory.rmdir()
	rmdir(Path("/tmp/researchAct.old"))

if __name__ == '__main__':
	main()