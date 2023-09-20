#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

# import all the necessary libraries
import boto3
import zipfile
import os

# define the function to deploy the lambda function
def deploy_lambda():
    
    # you can change the aws region, function folder and destination folder
    aws_region = 'us-east-2'
    function_folder = '/home/your_username/devops/lambda_function/lib/python3.10/site-packages'
    destination_folder = '/home/your_username/devops/lambda_function/'
    bucket_name = 'your_bucket_name'
    
    # change directory to the function folder
    os.chdir(function_folder)
    
    # get all the libraries in the function folder
    libraries = os.listdir(function_folder)
    
    # create a zip file with all the libraries
    with zipfile.ZipFile(destination_folder +  'lambda.zip', 'w') as zip:
        
        # write all the libraries to the zip file
        for library in libraries:
            zip.write(library)
    
    # change directory to the destination folder
    os.chdir(destination_folder)
    with open('lambda.zip', 'rb') as f:
        zip_file = f.read()
        
    # upload the zip file to s3
    s3_client = boto3.client('s3', region_name=aws_region)
    s3_client.put_object(
        Body=zip_file,
        Bucket=bucket_name,
        Key='lambda.zip'
    )
    
    
    # update the lambda function with the new zip file
    lambda_client = boto3.client('lambda', region_name=aws_region)
    lambda_client.update_function_code(
        FunctionName='your_lambda_function_name',
        S3Bucket=bucket_name,
        S3Key='lambda.zip'
    )
deploy_lambda()