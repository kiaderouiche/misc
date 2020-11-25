#!/usr/bin/bash
#

replacekeywords() {

for keywords in uri dir repo_uri srcuri module tarball_path
    do
        sed -i -e "s/\os.path.isdir($keywords)/\pathlib.Path($keywords).is_dir()/g" $1
        sed -i -e "s/\os.path.dirname($keywords)/\pathlib.Path($keywords).parent/g" $1
        sed -i -e "s/\os.path.basename($keywords)/\pathlib.Path($keywords).name/g" $1
        sed -i -e "s/\os.path.exists($keywords)/\pathlib.Path($keywords).exists()/g" $1
        sed -i -e "s/\os.path.isfile($keywords)/\pathlib.Path($keywords).is_file()/g" $1
        sed -i -e "s/os.getcwd/pathlib.Path.cwd/g" $1
    done
}
replacekeywords "./cvs.py"
