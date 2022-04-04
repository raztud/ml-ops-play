SHELL:=/bin/bash
# `errexit` ensures that the exit status of a command sequence will not be the last command but the last with a non-zero
# exit status, and that subsequent commands will not be executed
export SHELLOPTS        :=$(if $(SHELLOPTS),$(SHELLOPTS):)errexit



.PHONY: build-lint
build-lint:
	@echo "Build container for linting for project ${PROJECT}"
	docker build -f projects/${PROJECT}/Dockerfile . --build-arg project=${PROJECT} -t ${PROJECT}_test --target test
