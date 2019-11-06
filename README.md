# uncomp_s3_archive
Extracts and displays the archive in S3.

## usage
```
python uncomp_s3.py --help
usage: uncomp_s3.py [-h] [--profile [PROFILE]] path

required arguments:
  path                 example s3://mybucket/wawawa.zip

optional arguments:
  --profile [PROFILE]  Use a specific profile from your credential file.
```


## Demo
### tarfile
```
$ ls archive.tar.gz
archive.tar.gz

$ tar tvfz archive.tar.gz
-rw-rw-rw- kabegiwa/kabegiwa 7 2019-01-12 14:46 wawawa.txt
-rw-rw-rw- kabegiwa/kabegiwa 0 2019-11-07 07:15 sasasa.txt

$ aws s3 cp archive.tar.gz s3://mybucket/archive.tar.gz
$ aws s3 ls s3://mybucket/archive.tar.gz
2019-11-07 07:21:34        119 archive.tar.gz

$ python uncomp_s3.py s3://mybucket/archive.tar.gz
wawawa.txt
sasasa.txt
```

### zipfile
```
$ ls archive.zip
archive.zip

$ unzip -Z archive.zip
Archive:  archive.zip
Zip file size: 325 bytes, number of entries: 2
-rw-rw-rw-  3.0 unx        7 tx stor 19-Jan-12 14:46 wawawa.txt
-rw-rw-rw-  3.0 unx        0 bx stor 19-Nov-07 07:15 sasasa.txt
2 files, 7 bytes uncompressed, 7 bytes compressed:  0.0%

$ aws cp archive.tar.gz s3://mybucket/archive.zip
$ aws s3 ls s3://mybucket/archive.zip
2019-11-07 07:21:34        119 archive.zip

$ python uncomp_s3.py s3://mybucket/archive.zip
wawawa.txt
sasasa.txt
```