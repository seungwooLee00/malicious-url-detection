#!/bin/bash

URL="http://127.0.0.1:5000/predictJS"

JS_FILES=(test_flask/sample_scripts/*.js)

echo "JavaScript files to be sent:"
for JS_FILE in "${JS_FILES[@]}"
do
    echo "$JS_FILE"
done

CURL_COMMAND="curl -X POST $URL -H 'Content-Type: multipart/form-data'"

for JS_FILE in "${JS_FILES[@]}"
do
    CURL_COMMAND+=" -F 'files[]=@$JS_FILE'"
done

response=$(eval $CURL_COMMAND)

echo "Response from server:"
echo "$response"

