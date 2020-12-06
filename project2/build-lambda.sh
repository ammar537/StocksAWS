#!/bin/bash

PTON=python3
PIP=pip3
VENV=v-env
LAMBDA=quote_reader
IAM=080024501251

USAGE="Usage: $0 new|newboto|create|update|clean <lambda-func-name> <handler>"

if [ "$#" -ne 3 ]; then
    echo $USAGE
    exit
fi
LAMBDA=$2
HANDLER=$3

case $1 in

# Prepares a new deployment plain package
new)
    zip -g ${LAMBDA}.zip ${LAMBDA}.py           # Add lambda function code
    ;;
    
# Prepares a new deployment package including boto3 library (add as needed)
newboto)
    $PTON -m venv $VENV                         # Setup Python virtual environment
    source ${VENV}/bin/activate
    $PIP install boto3                          # Add non-standard packages (boto3 is the AWS SDK)
    cd ${VENV}/lib/python3.8/site-packages
    zip -r9 ${OLDPWD}/${LAMBDA}.zip .           # Zip up the packages
    cd ${OLDPWD}
    zip -g ${LAMBDA}.zip ${LAMBDA}.py           # Add labda function code
    deactivate
    ;;

# Prepares a new deployment package including boto3 library (add as needed)
newmem)
    $PTON -m venv $VENV                         # Setup Python virtual environment
    source ${VENV}/bin/activate
    $PIP install elasticache_auto_discovery     # Add non-standard packages (boto3 is the AWS SDK)
    $PIP install pymemcache
    cd ${VENV}/lib/python3.8/site-packages
    zip -r9 ${OLDPWD}/${LAMBDA}.zip .           # Zip up the packages
    cd ${OLDPWD}
    zip -g ${LAMBDA}.zip ${LAMBDA}.py           # Add labda function code
    deactivate
    ;;
    
# Creates a new AWS Lambda function from a deployment package
create)
    time aws lambda create-function --function-name ${LAMBDA}_${HANDLER} --zip-file fileb://${LAMBDA}.zip --handler ${LAMBDA}.${HANDLER} --runtime python3.8  --timeout 10 --memory-size 1024 --role arn:aws:iam::${IAM}:role/lambda-vpc-role \
    --cli-binary-format raw-in-base64-out \
    --vpc-config SubnetIds=subnet-b68597cc,SecurityGroupIds=sg-39f68148 \
    --cli-read-timeout 0 --cli-connect-timeout 0    # These parameters are optional for slower connections to prevent timeouts
    ;;

# Updates an existing AWS Lambda function 
update)
    zip -g ${LAMBDA}.zip ${LAMBDA}.py
    time aws lambda update-function-code --function-name ${LAMBDA}_${HANDLER} --zip-file fileb://${LAMBDA}.zip --cli-binary-format raw-in-base64-out \
    --cli-read-timeout 0 --cli-connect-timeout 0
    ;;
    
# Clean up temporary files
clean)
    rm -rf ~/.local/lib/python3.8/*
    rm -rf v-env
    rm $LAMBDA.zip
    ;;

*)
    echo $USAGE
    ;;
esac
