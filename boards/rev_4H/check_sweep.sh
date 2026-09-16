#!/bin/bash

if [[ ! "$(basename "$PWD")" == *run_sweep_* ]]
then
echo "Run this inside a run_sweep_#### dir as ../check_sweep.sh"
exit
fi

pushd $1
pwd
SEEDS=`find . -type d -maxdepth 1`
echo $SEEDS
for i in $SEEDS
do
if [ "$i" != "." ]
then
echo ================================
echo $i
echo ================================
pushd $i
../../check_timing.sh
../../check_resources.sh
popd
fi
done
