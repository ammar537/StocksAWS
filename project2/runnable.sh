# sudo apt-get install python3-venv
# sudo apt-get install python3-pip
# pip3 install elasticache-auto-discovery
# pip3 install python-memcached
# sudo apt-get install jq



# ./build-lambda.sh newmem stocks_project2 handler
# ./build-lambda.sh create stocks_project2 delete_ticker
# ./build-lambda.sh create stocks_project2 get_quotes
# ./build-lambda.sh create stocks_project2 get_quote
# ./build-lambda.sh create stocks_project2 add_quote
# ./build-lambda.sh create stocks_project2 get_tickers
# ./build-lambda.sh create stocks_project2 avg
# ./build-lambda.sh create stocks_project2 atr
# ./build-lambda.sh create stocks_project2 addfile
# ./build-lambda.sh create stocks_project2 get_ticker
# ./build-lambda.sh create stocks_project2 create_ticker


# aws apigatewayv2 create-api --name CloudComputing --protocol-type HTTP --target arn:aws:lambda:us-east-2:080024501251:function:stocks_project2_avg
api=$(aws apigatewayv2 create-api --name CloudComputing --protocol-type HTTP --target arn:aws:lambda:us-east-2:080024501251:function:stocks_project2_avg | jq ".ApiId" | tr -d '"')
echo $api
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /get_tickers' 
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /tickr/{ticker}/{name}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /tickr/{ticker}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /quotes/{ticker}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /quote/{ticker}/{datetime}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /avg/{ticker}/{datetime}/{period}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'GET /atr/{ticker}/{datetime}/{period}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'POST /create_ticker/{ticker}/{name}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'POST /add_qoute/{ticker}/{datetime}/{open}/{close}/{high}/{low}'
aws apigatewayv2 create-route --api-id ${api} --route-key 'DELETE /delete_ticker/{ticker}'