#!/usr/bin/bash
#

path="/home/jihbed/spaceWork/misc/pythonProj3/RepositoryHandler/repositoryhandler/backends"


for pyfile in $path/git.py $path/hg.py $path/cvs.py $path/svn.py $path/tarball.py
do
    echo "$pyfile Processing..." && wc -l $pyfile
    for keywords in uri dir repo_uri srcuri module tarball_path
    do
        sed -i -e "s/\os.path.isdir($keywords)/\pathlib.Path($keywords).is_dir()/g" $pyfile
        sed -i -e "s/\os.path.dirname($keywords)/\pathlib.Path($keywords).parent/g" $pyfile
        sed -i -e "s/\os.path.basename($keywords)/\pathlib.Path($keywords).name/g" $pyfile
        sed -i -e "s/\os.path.exists($keywords)/\pathlib.Path($keywords).exists()/g" $pyfile
        sed -i -e "s/\os.path.isfile($keywords)/\pathlib.Path($keywords).is_file()/g" $pyfile
        sed -i -e "s/os.getcwd/pathlib.Path.cwd/g" $pyfile
    done
done
