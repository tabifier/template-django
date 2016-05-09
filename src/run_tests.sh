#!/bin/bash
echo $@
set -e
source ../envs/testing && REUSE_DB=1 ./manage.py test $@
