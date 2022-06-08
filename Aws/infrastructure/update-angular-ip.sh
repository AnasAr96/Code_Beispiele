#!/bin/sh
ADDRESS=$1
#WORKING_DIR=$(pwd)
#
## check if argument has been passed
#if [ $# -eq 0 ]
#then
#    echo "No URL found as Parameter"
#    exit 1
#fi
#export AWS_PROFILE=haidi
#ADDRESS=$(aws ec2 describe-instances --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
#echo "Found IP: $ADDRESS"

ENVIRONMENT="export const environment = {\n"
ENVIRONMENT+="\tproduction: false,\n"
ENVIRONMENT+="\tNODE_API_URL: 'http://$ADDRESS:3333',\n"
ENVIRONMENT+="\tNODE_WS_URL: 'ws://$ADDRESS:3333'\n"
ENVIRONMENT+="};"

echo "[INFO] --- Overwriting environment.ts File..."

echo $ENVIRONMENT > ../../haidi-frontend/src/environments/environment.prod.ts
