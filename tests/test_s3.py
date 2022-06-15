from os.path import join as joinpath
import botocore.exceptions
from puddle import *

test_filename = 'TEST_a1d537d6'


def test_s3_download():
    path = get_object_from_s3(test_filename)
    assert path == joinpath(getenv('LOCAL_DATA_DIR'), test_filename)


def test_s3_delete():
    delete_object_from_s3(test_filename)
    try:
        get_object_from_s3(test_filename)
        assert False
    except botocore.exceptions.ClientError:
        assert True
    put_object_to_s3(dataset_id='TEST', filepath=joinpath(getenv('LOCAL_DATA_DIR'), test_filename))




