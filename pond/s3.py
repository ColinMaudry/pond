import boto3
from dotenv import load_dotenv
from os import getenv
from os.path import join

from .utils import *

load_dotenv()


def get_s3_session():
    """Get a valid S3 session from environment variables

    :return: An S3 session object
    """
    s3 = boto3.client('s3',
                      region_name=getenv('S3_REGION_NAME'),
                      endpoint_url=getenv('S3_API_ENDPOINT'),
                      aws_access_key_id=getenv("S3_ACCESS_KEY"),
                      aws_secret_access_key=getenv("S3_SECRET_KEY"))
    print(type(s3))
    return s3


def get_object_from_s3(object_key: str) -> str:
    """Downloads a file from the S3 bucket from its object key

    :param object_key:
    :return:
    """
    s3 = get_s3_session()
    filepath = join(getenv('LOCAL_DATA_DIR'), object_key)
    print("The file path: ", filepath)
    s3.download_file(getenv('S3_BUCKET_NAME'), object_key, filepath)
    return filepath


def put_object_to_s3(dataset_id: str, filepath: str) -> tuple:
    """Upload a new file to the S3 bucket

    :param dataset_id: The id of the dataset the file belongs to
    :param filepath: The path of the file to upload
    :return: S3 object key, sha1 checksum
    """
    s3 = get_s3_session()

    checksum = get_sha1sum_from_filepath(filepath)[:8]
    object_key = dataset_id + '_' + checksum
    with open(filepath, 'rb') as file:
        s3.upload_fileobj(file, getenv('S3_BUCKET_NAME'), object_key)
    return object_key, checksum


def delete_object_from_s3(object_key: str):
    s3 = get_s3_session()
    s3.delete_object(Bucket=getenv('S3_BUCKET_NAME'), Key=object_key)
