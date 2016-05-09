#! /bin/bash
ROLLING_UPDATE_SELECTOR=eu-api-web
SECRETS_SELECTOR=eu-api
ROLLING_UPDATE_PERIOD=1s
ROLLING_UPDATE_TEMPLATE=kubernetes/$ROLLING_UPDATE_SELECTOR-rc-rolling-update.yaml

################################################################################
#      DON'T CHANGE THE FOLLOWING UNLESS YOU KNOW WHAT YOU'RE DOING ;-)
################################################################################
SOURCE_DIR=`pwd`
cd `dirname $0`/..

# Steps:
# ------
# 1. delete secret
# 2. create secret
# 3. run rolling-update

SOURCE_DIR=`pwd`
cd `dirname $0`/..
SECRETS_FILE_PATH=$1
HOTFIX=$2
kubectl delete -f $SECRETS_FILE_PATH && \
kubectl create -f $SECRETS_FILE_PATH && \
deploy/rolling-update.sh "-secrets-update$HOTFIX"
cd $SOURCE_DIR
