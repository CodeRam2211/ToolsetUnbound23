import boto3
import numpy as np
import pandas as pd
import dask.dataframe as dd
import csv
from io import StringIO, BytesIO

s3 = ""

def setupS3():
    file=open('accesskey.csv')
    row = []
    reader = csv.reader(file)
    for i in reader:
        row.append(i)

    key_id = row[1][0]
    key = row[1][1]
    s3=boto3.client('s3',
                    aws_access_key_id =key_id,
                    aws_secret_access_key =key,
                    region_name = 'ap-south-1'
                    )
    s3_resource = boto3.resource('s3',
                                 aws_access_key_id =key_id,
                                aws_secret_access_key =key,
                                region_name = 'ap-south-1'
                                )
    session=boto3.Session(
                        aws_access_key_id =key_id,
                        aws_secret_access_key =key,
                        )
    bucket_name="toolset-unbound"
    return (s3,session)

def createfolder(id):
    s3,trash=setupS3()
    bucket_name="toolset-unbound"
    folder_name1 = id+"/text"
    s3.put_object(Bucket=bucket_name, Key=(folder_name1+'/'))
    folder_name2 = id+"/audio"
    s3.put_object(Bucket=bucket_name, Key=(folder_name2+'/'))
    folder_name3 = id+"/video"
    s3.put_object(Bucket=bucket_name, Key=(folder_name3+'/'))
    folder_name4 = id+"/images"
    s3.put_object(Bucket=bucket_name, Key=(folder_name4+'/'))
    return 'successful'
#createfolder('2')
def uploadfile(id,file_name,filetype):
    s3,trash=setupS3()
    uploadPath = (str(id)+'/'+filetype+'/'+str(file_name))
    try:
        s3.upload_file(file_name,"toolset-unbound",uploadPath)
    except :
        print("some errors encountered")
        return 0
    return 1

def listfiles(id,filetype):
    file_names=[]
    s3,session=setupS3()
    s3Resource = session.resource('s3')
    objects=s3.list_objects_v2(Bucket='toolset-unbound')
    my_bucket=s3Resource.Bucket('toolset-unbound')
    for objects in my_bucket.objects.filter(Prefix=id+"/"+filetype+"/"):
        file_names.append(objects.key)

    return file_names

def deletefile(id,file_name,filetype):
    s3,trash=setupS3()
    bucket_name='toolset-unbound'
    try:
        response=s3.delete_object(Bucket=bucket_name,Key=id+"/"+filetype+"/"+file_name)
    except:
        print("Unable to delete file")
        return 0
    return 1

def downloadfile(id,file_name,filetype):
    s3,trash=setupS3()
    try:
        s3.download_file('toolset-unbound',str(id)+'/'+file_name+'/'+file_name,file_name)
    except:
        print("Unable to download file")
        return 0
    return 1
uploadfile('1','accesskey.csv',"text")
listfiles("text")