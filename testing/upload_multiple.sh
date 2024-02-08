#! /bin/bash
while getopts i:t: flag
do
    case "${flag}" in
        i) i=${OPTARG};;
        t) t=${OPTARG};;
    esac
done

while [ $i -le $t ]
do
    python Main_v4.py $i;
    ((i++));
    sleep 1;
done
