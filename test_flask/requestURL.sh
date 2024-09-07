#!/bin/bash

URL="http://127.0.0.1:5000/predictURL"

URL_FILES=(test_flask/sample_urls/*)

echo "url files to be sent:"
for URL_FILE in "${URL_FILES[@]}"
do
    echo "$URL_FILE"
done

CURL_COMMAND="curl -X POST $URL -H 'Content-Type: multipart/form-data'"

for URL_FILE in "${URL_FILES[@]}"
do
    CURL_COMMAND+=" -F 'files[]=@$URL_FILE'"
done

response=$(eval $CURL_COMMAND)

echo "Response from server:"
echo "$response"

