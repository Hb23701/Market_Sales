import boto3
from .constants import BUCKET_NAME

def s3_bucket():
    s3 = boto3.client('s3')
    return s3.Bucket(BUCKET_NAME)

def download_files_from_s3(date):
    global date_format
    date_format = date.strftime("%Y%m%d")
    n = 1
    while True:
        try:
            s3_bucket().download_file(f"/{date_format}/Transaction_{date_format}_{n}.csv", f"tmp/{date_format}/Transaction_{date_format}_{n}.csv")
            n += 1
        except:
            break