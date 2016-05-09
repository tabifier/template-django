for envar in `find /secrets -follow -type f`; do export $(cat $envar); done
