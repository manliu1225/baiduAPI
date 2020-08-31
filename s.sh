#! /bin/bash

#FILES="$(ls -1 *.txt)"
INPUT_DIR="${1}"
OUTPUT_DIR="${2}"

mkdir -p ${OUTPUT_DIR}

FILES="$(find ${INPUT_DIR} -name '*.txt')"

I="1"
for FILE in ${FILES}; do
#BASE="$(basename ${FILE} .txt)"
  NUM="$(printf "%06d" ${I})"
  cp ${FILE} ${OUTPUT_DIR}/${NUM}.txt
  I="$((${I} + 1))"
done
