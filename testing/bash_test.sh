#! /bin/bash
while getopts i:t: flag
do
    case "${flag}" in
        i) i=${OPTARG};;
        t) t=${OPTARG};;
    esac
done

echo $i;
echo $t;
