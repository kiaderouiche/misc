#!/usr/bin/bash
#

replacekeywords() {

echo " ==> $2 enter..."
echo "$1 Processing..."
sed -i -e "s/\os.path.isdir(path)/\pathlib.Path(path).is_dir()/g" "$2"
sed -i.bak -e "s/\os.path.dirname("$1")/\pathlib.Path("$1").parent/g" "$2"
sed -i.bak -e "s/\os.path.basename("$1")/\pathlib.Path("$1").name/g" "$2"
sed -i.bak -e "s/\os.path.exists("$1")/\pathlib.Path("$1").exists()/g" "$2"
sed -i.bak -e "s/\os.path.isfile("$1")/\pathlib.Path("$1").is_file()/g" "$2"
sed -i.bak -e "s/os.getcwd/pathlib.Path.cwd/g" "$2"
}

for keywords in "path" "uri" "srcuri" "srcdir"
do
    replacekeywords $keywords "cvs.py"
done

