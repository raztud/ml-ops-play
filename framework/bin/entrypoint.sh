#!/usr/bin/env bash

entrypoint=$1
arguments=${@:2}

function test_by_tag {
  tag=$1
  echo "Running tests with tag '$1' for ${PROJECT}"
  pytest ${PROJECT} -m "${tag}"

  local status=$?
  if [ $status -eq 5 ]; then
      echo "No tests with tag ${tag}"
      return 0
  fi

  return $status
}

case "$entrypoint" in
  "lint")
    flake8 "${PROJECT}" ${arguments}
    ;;
  "test")
    test_by_tag ${arguments}
    ;;
  "train")
    python "${WORKDIR}/${PROJECT}/train.py" ${arguments}
    ;;

  "serve")
    uvicorn main:app --reload --port 8080 --app-dir=${WORKDIR}/${PROJECT}/api
    ;;
  "")
    echo "You must specify a command as an argument. For instance, try 'train'"
    exit 1
    ;;
  *)
    echo "Command $entrypoint is not a valid command for the entrypoint script"
    exit 1
    ;;
esac