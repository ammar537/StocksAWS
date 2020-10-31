#!/bin/bash

sudo apt-get install jq
sudo apt install python3-virtualenv
virtualenv v-env
source v-env/bin/activate
pip install Pillow boto3
cd $VIRTUAL_ENV/lib/python3.8/site-packages
zip -r9 ${OLDPWD}/lambda.zip .
cd ${OLDPWD}
zip -g lambda.zip funt1_down.py Average.py
deactivate
role=rolepolicy26

IMA=`aws iam create-role --role-name $role --assume-role-policy-document '{
                "Version": "2012-10-17",
                "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                        "Service": "lambda.amazonaws.com"

                },
                "Action":  "sts:AssumeRole"
            }
                ]
        }' | jq -r .Role.Arn`

aws iam attach-role-policy --role-name $role --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess
aws iam attach-role-policy --role-name $role --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess
aws iam attach-role-policy --role-name $role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name $role --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name $role --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess

aws lambda create-function --function-name function1 \
--zip-file fileb://lambda.zip --handler funt2.lambdaHandler --runtime python3.8 \
--timeout 45 --memory-size 1024 \
--role arn:aws:iam::244450108036:role/$role

aws lambda create-function --function-name function2 \
--zip-file fileb://lambda.zip --handler funt1.lambdaHandler --runtime python3.8 \
--timeout 45 --memory-size 1024 \
--role arn:aws:iam::244450108036:role/$role