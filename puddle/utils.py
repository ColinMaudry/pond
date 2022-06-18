from os import getenv, rename
from os.path import join


def download_file(url: str, dataset_series_id: str, fileext: str) -> dict:
    from requests import get
    import email.utils as eut

    download = get(url, allow_redirects=True)
    temp_hash = get_sha1sum_from_string(download.url + download.headers['date'])

    temp_filepath = join(getenv('LOCAL_DATA_DIR'), temp_hash)
    with open(temp_filepath, 'wb') as file:
        file.write(download.content)

    final_hash = get_sha1sum_from_filepath(temp_filepath)
    final_filename = f'{dataset_series_id}_{final_hash[:8]}.{fileext}'
    final_filepath = join(getenv('LOCAL_DATA_DIR'), final_filename)
    rename(temp_filepath, final_filepath)

    return {
        'sizeInBytes': int(download.headers['content-length']),
        'date': eut.parsedate_to_datetime(download.headers['date']).isoformat(),
        'filepath': final_filepath,
        'filename': final_filename,
        'sha1sum': final_hash
    }


def get_sha1sum_from_filepath(filepath: str) -> str:
    from hashlib import sha1
    """Generate sha1 checkup from a file path.

    :param filepath: The path of the file
    :return: The SHA1 checksum of the provided file.
    """
    with open(filepath, 'rb') as file:
        sha1sum = sha1()
        while True:
            chunk = file.read(16 * 1024)
            if not chunk:
                break
            sha1sum.update(chunk)
        return sha1sum.hexdigest()


def get_sha1sum_from_string(string: str) -> str:
    from hashlib import sha1
    sha1sum = sha1()
    encoded_string = string.encode(encoding='UTF-8', errors='strict')
    sha1sum.update(encoded_string)
    return sha1sum.hexdigest()


