pip freeze --local |sed -rn 's/^([^=# \t\\][^ \t=]*)=.*/echo; echo Processing \1 ...; pip install -U \1/p' |sh
pip install -U `yolk -U | awk '{print $1}' | uniq`
