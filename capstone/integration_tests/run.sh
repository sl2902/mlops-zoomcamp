#!/usr/bin/env bash

cd "$(dirname "$0")"

function print_info {
    RESET="\e[0m"
    BOLD="\e[1m"
    YELLOW="\e[33m"
    echo -e "$YELLOW$BOLD [+] $1 $RESET"
}

export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin
export AWS_REGION=eu-west-1
export AWS_DEFAULT_REGION=eu-west-1
export AWS_ACCESS_KEY_ID=In1IKgTRbO9U4yPK
export AWS_SECRET_ACCESS_KEY=Ee2p53DTNVczXbZ62JLOBAzHAQ4cOnyY
export POSTGRES_DB=mlflowdb
export POSTGRES_USER=user
export POSTGRES_PASSWORD=password
export EXPERIMENT_NAME=test-credit-churn-experiment

print_info "Creating MLOps test pipeline"
docker-compose up --build -d

if [[ $? -eq 0 ]]; then
    print_info "Pipeline ready to accept requests"
else
    unset EXPERIMENT_NAME
    docker-compose logs
    docker-compose down -v
    docker-compose down --rmi=all
fi

print_info "Run prefect training workflow"
docker exec -t test_prefect python train.py

ERROR_CODE=$?

if [[ $? -ne 0 ]]; then
    docker-compose logs
    docker-compose down
    exit $?
fi

sleep 10

print_info "Reload model"
docker restart test_app

sleep 5

print_info "Test model serving"
python test_predict.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

print_info "Clean up"
docker-compose down -v
docker-compose down --rmi=all