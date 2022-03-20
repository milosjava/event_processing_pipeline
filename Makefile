# Name of the local application docker container.
IMAGE=event_processing_pipeline

all: test
test:
	poetry run coverage run --omit=tests/* -m unittest tests/*.py && poetry run coverage xml

# Build the application container.
docker:
	DOCKER_BUILDKIT=1 \
		docker build -f Dockerfile -t "${IMAGE}:latest" .

run-docker:
	docker run -p 5000:5000 "${IMAGE}:latest"


