import boto3
from botocore.exceptions import ClientError
import zipfile
import tarfile
from io import BytesIO
import argparse
import copy
import sys

class uncomp():
    def __init__(self, path, profile='default'):
        self.session = boto3.Session(profile_name=profile)
        self.s3 = self.session.resource('s3')
        try:
            self.path_list = path[5:].split('/')
            self.bucket_name = self.path_list[0]
            self.file_name = "/".join(self.path_list[1:])  
            self.object = BytesIO(self.s3.Object(bucket_name=self.bucket_name, key=self.file_name).get()["Body"].read())
            self.tmp_object = copy.copy(self.object)
        except ClientError :
            print('No such key.')
            sys.exit(1)
    
    def auto(self, flag=''):
        try:
            if zipfile.is_zipfile(self.tmp_object):
                flag = 'zip'
            else :
                flag = 'tar'
        except:
            print(self.file_name)
            sys.exit(0)
        return flag

class zip(uncomp):
    def __init__(self, path, profile='default'):
        super().__init__(path, profile)

    def print_obj(self):    
        zip = zipfile.ZipFile(self.object)
        for filename in zip.namelist():
            print(filename)


class tar(uncomp):
    def __init__(self, path, profile='default'):
        super().__init__(path, profile)

    def print_obj(self):
        tar = tarfile.open(fileobj=self.object)
        for filename in tar.getnames():
            print(filename)
        tar.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__)
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('path', help='example s3://mybucket/archive.zip', type=str)
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--profile',nargs='?',default='default',help='Use a specific profile from your credential file.') 
    args = parser.parse_args()
    path = args.path
    profile = args.profile

    if uncomp(path, profile).auto() == 'zip':
        zip(path, profile).print_obj()
    else:
        tar(path, profile).print_obj()
    

