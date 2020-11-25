#!/usr/bin/bash
#

replacekeywords() {

echo " ==> $1 enter..."
echo "$1 Processing..."
for texpr in "path" "uri" "srcuri" "srcdir" "module" "repo_uri"
do
    sed -i -e "s/\os.path.isdir($texpr)/\pathlib.Path($texpr).is_dir()/g" $1
    sed -i.bak -e "s/\os.path.dirname($texpr)/\pathlib.Path($texpr).parent/g" $1
    sed -i.bak -e "s/\os.path.basename($texpr)/\pathlib.Path($texpr).name/g" $1
    sed -i.bak -e "s/\os.path.exists($texpr)/\pathlib.Path($texpr).exists()/g" $1
    sed -i.bak -e "s/\os.path.isfile($texpr)/\pathlib.Path($texpr).is_file()/g" $1
    sed -i.bak -e "s/os.getcwd/pathlib.Path.cwd/g" $1
    sed -i.bak -e "s/os.path.join/pathlib.Path().joinpath/g" $1
    sed -i.bak -e "s/\os.makedirs($texpr)/\pathlib.Path($texpr).mkdir()/g" $1
done

}

for pyfile in "cvs.py" "git.py" "hg.py" "svn.py" "tarball.py" "bzr.py"
do
    replacekeywords $pyfile
done


