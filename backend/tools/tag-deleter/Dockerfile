FROM debian

ENV IMAGE_REGISTRY_URL=hub.docker.com
ENV IMAGE_REGISTRY_CI_USER=
ENV IMAGE_REGISTRY_CI_PASSWORD=
ENV CI_COMMIT_SHA=
ENV USE_TOKEN=

RUN apt-get update && apt-get upgrade -y && apt-get install -y curl jq
COPY delete_tag.sh .
RUN chmod +x delete_tag.sh

CMD ["./delete_tag.sh"]
