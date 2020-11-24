#!/usr/bin/bash
#

keywordsReplace(){
for keywords in uri dir repo_uri srcuri module tarball_path
    do
        sed -i -e "s/\os.path.isdir($keywords)/\pathlib.Path($keywords).is_dir()/g" $1
        sed -i -e "s/\os.path.dirname($keywords)/\pathlib.Path($keywords).parent/g" $1
        sed -i -e "s/\os.path.basename($keywords)/\pathlib.Path($keywords).name/g" $1
        sed -i -e "s/\os.path.exists($keywords)/\pathlib.Path($keywords).exists()/g" $1
        sed -i -e "s/\os.path.isfile($keywords)/\pathlib.Path($keywords).is_file()/g" $1
    done
}

for pyfile in [a-t]*.py
do
    if [ "$pyfile" == "git.py" ] 
    then
        echo "$pyfile Processing..."
        #function
        keywordsReplace "./$pyfile"
        #Exception
        sed -i -e "s/\os.path.dirname(directory)/\pathlib.Path(directory).parent/g" "./$pyfile"
        sed -i -e "s/\os.path.isdir(pathlib.Path().joinpath(dir, ".git"))/\pathlib.Path(pathlib.Path().joinpath(dir, ".git")).isdir()/g" "./$pyfile"
        sed -i -e "s/\os.path.basename(self.uri.rstrip('/'))/\pathlib.Path(self.uri.rstrip('/')).name()/g" "./$pyfile"
        sed -i -e "s/\os.path.basename(uri.rstrip('/'))/\pathlib.Path(uri.rstrip('/')).name()/g" "./$pyfile"
    fi
    
    if [ "$pyfile" == "svn.py" ]
    then
        echo "$pyfile Processing..."
        #function
        keywordsReplace "./$pyfile"
        #Exception
        sed -i -e "s/\os.path.basename(uri.rstrip('/'))/\pathlib.Path(uri.rstrip('/')).name/g" "./$pyfile"
        sed -i -e "s/\os.path.basename(self.uri.rstrip('/'))/\pathlib.Path(self.uri.rstrip('/')).name/g" "./$pyfile"
        sed -i -e "s/\os.path.join/\pathlib.Path().joinpath/g" "./$pyfile"
    fi
    
    if [ "$pyfile" == "hg.py" ]
    then
        echo "$pyfile Processing..."
    #function
    keywordsReplace "./$pyfile"
    fi
    
    if [ "$pyfile" == "cvs.py" ]
    then
        echo "$pyfile Processing..."
        #function
        keywordsReplace "./$pyfile"
        #Exception
        sed -i -e "s/\os.path.join/\pathlib.Path().joinpath/g" "./$pyfile"
    fi
    
    if [ "$pyfile" == "tarball.py" ]
    then
        echo "$pyfile Processing..."
        #function
        keywordsReplace "./$pyfile"
        #Exception
        sed -i -e "s/\os.path.join/\pathlib.Path().joinpath/g" "./$pyfile"
    fi
    
    if [ "$pyfile" == "bzr.py" ]
    then
        echo "$pyfile Processing..."
        #function
        keywordsReplace "./$pyfile"
    fi
        sed -i -e "s/\os.path.join/\pathlib.Path().joinpath/g" "./$pyfile"
done
