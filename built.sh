docker buildx build --platform linux/amd64 -t metering .
docker save metering > image.tar
zip metering cumulocity.json image.tar