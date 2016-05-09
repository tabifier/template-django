#! /bin/bash

rollingDeploy() {
  ROLLING_UPDATE_SELECTOR=$1
  ROLLING_UPDATE_PERIOD=$2
  ROLLING_UPDATE_TEMPLATE=kubernetes/$ROLLING_UPDATE_SELECTOR-rc-rolling-update.yaml

  ################################################################################
  #      DON'T CHANGE THE FOLLOWING UNLESS YOU KNOW WHAT YOU'RE DOING ;-)
  ################################################################################
  # Exit on any error
  set -e

  KUBE_CMD=kubectl

  HOTFIX=$3
  GIT_SHA1=$(git rev-parse HEAD | cut -c1-15)
  GIT_SHA1=$GIT_SHA1$HOTFIX
  CURRENT_RC=$($KUBE_CMD get rc --selector=app=$ROLLING_UPDATE_SELECTOR --output='jsonpath={.items[*].metadata.name}')
  cp $ROLLING_UPDATE_TEMPLATE deploy-rc.yaml && \
  sed -i.bak s/VERSION/$GIT_SHA1/g deploy-rc.yaml && \
  $KUBE_CMD rolling-update $CURRENT_RC --show-all --update-period=$ROLLING_UPDATE_PERIOD -f deploy-rc.yaml && \
  rm deploy-rc.yaml*
  STATUS=$?
  if [[ $STATUS != 0 ]]; then exit $STATUS; fi
}

SOURCE_DIR=`pwd`
cd `dirname $0`/..

rollingDeploy 'eu-api-web' 1s $1
rollingDeploy 'eu-api-worker' 30s $1
cd $SOURCE_DIR
exit 0
