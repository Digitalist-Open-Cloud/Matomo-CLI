VERSION=$(grep '^version' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

docker tag digitalist/matomo-cli digitalist/matomo-cli:$VERSION
docker push digitalist/matomo-cli
docker push digitalist/matomo-cli:$VERSION

docker tag digitalist/matomo-exporter digitalist/matomo-exporter:$VERSION
docker push digitalist/matomo-exporter
docker push digitalist/matomo-exporter:$VERSION