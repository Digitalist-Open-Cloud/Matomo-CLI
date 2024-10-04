VERSION=$(grep '^version' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

docker build --build-arg RELEASE=${VERSION} -f Dockerfile.cli . -t digitalist/matomo-cli --no-cache --platform=linux/amd64
docker build --build-arg RELEASE=${VERSION} -f Dockerfile.prometheus . -t digitalist/matomo-exporter --no-cache --platform=linux/amd64