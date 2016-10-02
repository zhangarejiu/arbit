#!/usr/bin/env bash

mongoexport --db arbit --collection form4 --out form4.json
mongoexport --db arbit --collection fundamentals --out fundamentals.json
mongoexport --db arbit --collection ratingsChanges --out ratingsChanges.json
mongoexport --db arbit --collection symbols --out symbols.json
mongoexport --db arbit --collection yahooQuotes --out yahooQuotes.json

# reformat the json in a way BigQuery will like
python3 converToBigQueryFormat.py

# copy everything to a bucket so we can import it to BigQuery
gsutil cp *.bigquery gs://mongoexport
