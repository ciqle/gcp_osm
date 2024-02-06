#!/bin/bash
set -e
CSV_FILES_PATH="$1"
SCRIPT_TYPE="$2"

if [ $# -ne 2 ];
then
  echo "Usage: $0 <CSV_FILES_PATH> <SCRIPT_TYPE>"
  exit 1
fi

for csv_file in $(ls -d ${CSV_FILES_PATH}*.geojson.csv);
do
  echo "Currently processing file: ${csv_file}"
  if [ ${SCRIPT_TYPE} == "py" ];
  then
    cat ${csv_file} \
    | python csv_to_json/csv2json.py \
    2> ${csv_file}.errors.jsonl > ${csv_file}.jsonl
  elif [ ${SCRIPT_TYPE} == "perl" ]; then
    cat ${csv_file} \
    | perl csv_to_json/geojson-csv-to-json.pl \
    2> ${csv_file}.errors.jsonl > ${csv_file}.jsonl
  fi
done
