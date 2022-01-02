#!/bin/bash

USERNAME=$IMAGE_REGISTRY_CI_USER
PASSWORD=$IMAGE_REGISTRY_CI_PASSWORD
ORGANIZATION=$IMAGE_REGISTRY_CI_USER
IMAGE=$CI_PROJECT_NAME
TAG=$CI_COMMIT_SHA
URL=$IMAGE_REGISTRY_URL

login_data() {
cat <<EOF
{
  "username": "$USERNAME",
  "password": "$PASSWORD"
}
EOF
}

if [[ -z $USE_TOKEN ]]; then
    curl --user $USER:$PASSWORD -X DELETE "https://${URL}/v2/${ORGANIZATION}/${IMAGE}/manifests/$(
        curl --user $USER:$PASSWORD -I \
            -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
            "https://${URL}/v2/${ORGANIZATION}/${IMAGE}/manifests/${TAG}" \
        | awk '$1 == "docker-content-digest:" { print $2 }' \
        | tr -d $'\r' \
    )"
else
    TOKEN=`curl -s -H "Content-Type: application/json" -X POST -d "$(login_data)" "https://$URL/v2/users/login/" | jq -r .token`
    curl "https://$URL/v2/repositories/${ORGANIZATION}/${IMAGE}/tags/${TAG}/" -f -L -X DELETE -H "Authorization: Bearer ${TOKEN}"
fi
