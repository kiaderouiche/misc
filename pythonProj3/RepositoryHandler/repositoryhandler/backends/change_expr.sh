#!/usr/bin/bash
#

changeExpr() {
echo "$1"
    sed -i -e "s/\os.path.isdir(path)/\pathlib.Path(path).is_dir()/g" $1
}

changeExpr "cvs.py"
