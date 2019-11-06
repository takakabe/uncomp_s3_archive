import boto3
import zipfile
import gzip
import tarfile
from io import BytesIO
import argparse
import re
import copy

class uncomp():
    def __init__(self, path):    
        self.path_list = path[5:].split('/')
        self.bucket_name = self.path_list[0]
        self.file_name = self.path_list[-1]
        self.zip_obj = BytesIO(s3.Object(bucket_name=self.bucket_name, key=self.file_name).get()["Body"].read())
        self.tmp_zip_obj = copy.copy(self.zip_obj)
        
        if zipfile.is_zipfile(self.tmp_zip_obj):
            self.zip()
        else:
            self.tar()

    def zip(self):    
        zip = zipfile.ZipFile(self.zip_obj)
        for filename in zip.namelist():
            file_info = zip.getinfo(filename)
            print(filename)

    def tar(self):
        tar = tarfile.open(fileobj=self.zip_obj)
        for filename in tar.getnames():
            print(filename)
        tar.close()

if __name__ == '__main__':
    s3 = boto3.resource('s3')

    parser = argparse.ArgumentParser(prog=__file__)
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('path', help='example s3://mybucket/wawawa.zip', type=str)
    #optional = parser.add_argument_group('optional arguments')
    #optional.add_argument('--name', default='ALL', help='Name of AWS account (default: ALL)')
    args = parser.parse_args()
    
    uncomp(args.path)

