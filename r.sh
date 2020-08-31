#! /bin/bash

FILES="$(ls -1 *.txt)"

I="1"
for FILE in ${FILES}; do
  BASE="$(basename ${FILE} .txt)"
  NUM="$(printf "%06d" ${I})"
  mv ${FILE} ${NUM}.txt
  I="$((${I} + 1))"
done
