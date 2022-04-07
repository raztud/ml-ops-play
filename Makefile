SHELL:=/bin/bash
# `errexit` ensures that the exit status of a command sequence will not be the last command but the last with a non-zero
# exit status, and that subsequent commands will not be executed
export SHELLOPTS        :=$(if $(SHELLOPTS),$(SHELLOPTS):)errexit
SERVE_PORT 				:= 8080


.PHONY: build-lint
build-lint:
	@echo "Build container for linting for project ${PROJECT}"
	docker build -f projects/${PROJECT}/Dockerfile . --build-arg project=${PROJECT} -t ${PROJECT}_test --target test

build-serve:
	 docker build -f projects/${PROJECT}/Dockerfile . --build-arg project=${PROJECT} -t ${PROJECT}_serve --target serve

serve:
	@echo "Running API on http://localhost:${SERVE_PORT}"
	docker run -p ${SERVE_PORT}:8080 -e S3_BUCKET -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY ${PROJECT}_serve:latest serve
