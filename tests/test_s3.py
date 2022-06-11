from os.path import join as joinpath
import botocore.exceptions
from pond import *


def test_s3_download():
    path = get_object_from_s3('TEST_a1d537d6')
    assert path == joinpath(getenv('LOCAL_DATA_DIR'), 'TEST_a1d537d6')


def test_s3_delete():
    delete_object_from_s3('TEST_a1d537d6')
    try:
        get_object_from_s3('TEST_a1d537d6')
        assert False
    except botocore.exceptions.ClientError:
        assert True
    put_object_to_s3('TEST', joinpath(getenv('LOCAL_DATA_DIR'), 'TEST_a1d537d6'))




