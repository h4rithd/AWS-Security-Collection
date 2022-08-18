#!/bin/bash

token_file=$1
profile_name=$2

if grep -q "$profile_name" ~/.aws/credentials; then
    echo ""
    echo "[ERROR] Profile $profile_name is existing on the ~/.aws/credentials"
else
    cp $token_file /tmp/aws_token

    sed -i 's/\\n/\n/g' /tmp/aws_token
    AccessKey=$(grep -i "AWS_ACCESS_KEY_ID" /tmp/aws_token | awk -F= '{print $2}')
    SecretKey=$(grep -i "AWS_SECRET_ACCESS_KEY" /tmp/aws_token | awk -F= '{print $2}')
    SessionToken=$(grep -i "AWS_SESSION_TOKEN" /tmp/aws_token | awk -F= '{print $2}')

    rm -rf /tmp/aws_token

    echo "" >> ~/.aws/credentials
    echo "[$profile_name]" >> ~/.aws/credentials
    echo "aws_access_key_id = $AccessKey" >> ~/.aws/credentials
    echo "aws_secret_access_key = $SecretKey" >> ~/.aws/credentials
    echo "aws_session_token = $SessionToken" >> ~/.aws/credentials
    echo "" >> ~/.aws/credentials
    echo ""
    echo "[SUCCESS] - $profile_name - Profile has been created!"
fi
