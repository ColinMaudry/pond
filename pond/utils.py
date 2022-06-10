from hashlib import sha1


def get_sha1sum_from_filepath(filepath: str) -> str:
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
