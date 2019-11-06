import boto3
from botocore.exceptions import ClientError
import zipfile
import tarfile
from io import BytesIO
import argparse
import re
import copy
import sys

class uncomp():
    def __init__(self, path):    
        try:
            self.path_list = path[5:].split('/')
            self.bucket_name = self.path_list[0]
            self.file_name = self.path_list[-1]
            self.object = BytesIO(s3.Object(bucket_name=self.bucket_name, key=self.file_name).get()["Body"].read())
            self.tmp_object = copy.copy(self.object)
        except ClientError :
            print('No such key.')
            sys.exit(1)

        try:
            if zipfile.is_zipfile(self.tmp_object):
                self.zip()
            else :
                self.tar()
        except:
            print(self.file_name)
            sys.exit(1)

    def zip(self):    
        zip = zipfile.ZipFile(self.object)
        for filename in zip.namelist():
            file_info = zip.getinfo(filename)
            print(filename)

    def tar(self):
        tar = tarfile.open(fileobj=self.object)
        for filename in tar.getnames():
            print(filename)
        tar.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__)
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('path', help='example s3://mybucket/wawawa.zip', type=str)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--profile',nargs='?',default='default',help='Use a specific profile from your credential file.') 

    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile)
    s3 = session.resource('s3')

    uncomp(args.path)

