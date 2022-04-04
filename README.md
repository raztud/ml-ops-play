## Commands 

###### build container
1. `export PROJECT=lifestat`
2. `docker build -f projects/lifesat/Dockerfile . --build-arg project=lifesat -t ${PROJECT}`

###### go into container
`docker run -it --entrypoint bash ${PROJECT}`

###### local useful tricks
1. set PYTHONPATH

```
export MLPOPS_PATH=/path/to/the/project
export PYTHONPATH=$PYTHONPATH:${MLPOPS_PATH}/projects/lifesat/src/:${MLPOPS_PATH}
```

2. train locally

`S3_BUCKET="razvan..." AWS_PROFILE=razvan-console-... python projects/lifesat/src/train.py`

###### start the train inside docker
1. go into docker, set the AWS_* env variables
2. `S3_BUCKET="..." python lifesat/train.py --version=1.2`

###### train using docker container
1. build container
2. 
   1. `docker run ${PROJECT} train --version=23`
   2. with inject necessary env variables: 
   ```
   export AWS_ACCESS_KEY_ID=... 
   export AWS_SECRET_ACCESS_KEY=...
   export S3_BUCKET=...
   docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e S3_BUCKET ${PROJECT} train --version=12
   ```

##### testing/linting in docker
1. `export PROJECT=lifesat`
2. `docker build -f projects/${PROJECT}/Dockerfile . --build-arg project=${PROJECT} -t ${PROJECT}_test --target test`
3. 
   1. `docker run ${PROJECT}_test lint`
   2. `docker run ${PROJECT}_test test unit`


##### start the API
```bash
$ # eg: export PROJECT="livesat"
$ export PYTHONPATH=${PYTHONPATH}:</full/path/to>/projects/${PROJECT}/src/
$ cd projects/${PROJECT}/src/api
$ uvicorn main:app --reload --port 8080
# or
$ python main.py
```
Run http call:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "gdp": 22587
}'
```

Expected response:
```JSON
{
  "prediction": 5.962423376619663
}
```


## TODO
- <strike>docker command to train, lint, unit test</strike>
- <strike>github action to run lint</strike>
- <strike>metrics support</strike>
- ecr repo
- github action to build a docker image

# Architecture

This framework allows to easily train and serve predictions for different ML models.
Features:
- build training container
- support for S3 upload and download of the training artifacts
- testing container
- serving API based on FastAPI (todo: container)
- support for metrics (time to respond, count)
