#!/bin/bash


if [ $# -eq 0 ]
		then echo "Upload file"
		exit 0
fi

region=us-east-1
bucket=mfff-alice-upload
lamda1=function1
lamda2=function2

lamda1_arn=`aws lambda get-function-configuration --function-name $lamda1 --region $region | jq -r .FunctionArn`
lamda2_arn=`aws lambda get-function-configuration --function-name $lamda2 --region $region | jq -r .FunctionArn`
sync_arn=`aws sns create-topic --name alice-SYNC | jq -r .TopicArn`

aws lambda add-permission --function-name $lamda1 --principal s3.amazonaws.com --statement-id s3invoke --action "lambda:InvokeFunction" --source-arn arn:aws:s3:::$bucket --source-account 244450108036
aws lambda add-permission --function-name $lamda2 --source-arn $sync_arn --statement-id sns-same-account --action "lambda:InvokeFunction" --principal sns.amazonaws.com

aws s3 mb s3://$bucket/alice-$@ --region $region
aws s3api put-bucket-notification-configuration --bucket $bucket --notification-configuration '{"LambdaFunctionConfigurations": [{"Id":"Uploader","LambdaFunctionArn":"'$lamda1_arn'","Events":["s3:ObjectCreated:Put"]}]}'
aws s3 cp $@ s3://$bucket/alice-$@	

aws sns subscribe --protocol lambda --topic-arn $sync_arn --notification-endpoint $lamda2_arn
aws sns publish --topic-arn $sync_arn --message "[alice,$@,10,CLOSE]"


