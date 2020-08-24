GoPdfc --  Golang PDF Compressor
====================================

Simple golang program on command line to compress PDF.

Installation
-------------
* Install dependency Ghostscript.
On Windows: install binaries via [official website] (https://www.ghostscript.com/)


Usage
-----
`pdfc [-o output_file_path] [-c number] input_file_path`

Ex:
`pdfc -o out.pdf in.pdf`

Output:
```
Compress PDF...
Compression by 65%.
Final file size is 1.4MB
Done.
```

Options
-------
* `-c` or `--compress` specifies 5 levels of compression, similar to standard pdf generator level:
  * 0: default
  * 1: prepress
  * 2: printer
  * 3: ebook
  * 4: screen
* `-o`or `--out` specifies the output file path. If not specified, input file will be erased.
* `-b`or `--backup` creates a backup of the original file in case no output is specified to avoid erasing the original file.
