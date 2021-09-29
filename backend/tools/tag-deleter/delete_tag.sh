#!/bin/bash

USERNAME=$IMAGE_REGISTRY_CI_USER
PASSWORD=$IMAGE_REGISTRY_CI_PASSWORD
ORGANIZATION=$IMAGE_REGISTRY_CI_USER
IMAGE=$CI_PROJECT_NAME
TAG=$CI_COMMIT_SHA

login_data() {
cat <<EOF
{
  "username": "$USERNAME",
  "password": "$PASSWORD"
}
EOF
}

TOKEN=`curl -s -H "Content-Type: application/json" -X POST -d "$(login_data)" "https://hub.docker.com/v2/users/login/" | jq -r .token`

curl "https://hub.docker.com/v2/repositories/${ORGANIZATION}/${IMAGE}/tags/${TAG}/" \
-X DELETE \
-H "Authorization: JWT ${TOKEN}"
