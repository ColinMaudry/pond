import botocore.exceptions
import rdflib
from rdflib import Graph
from rdflib.namespace import DCAT
from os import getenv
from .s3 import get_object_from_s3, put_object_to_s3
from dotenv import load_dotenv
from os.path import join
import os

load_dotenv()


def create_new_store() -> rdflib.Graph:
    """ Create a blank metadata store in memory.

    :return: A blank metadata store.
    :rtype: rdflib.Graph
    """
    graph = Graph()
    graph.bind('dcat', DCAT)
    return graph


def load_store(rdf_filepath: str) -> rdflib.Graph:
    """Load the local metadata store in memory.

    :param rdf_filepath: The file path to the RDF file.
    :return: rdflib.Graph
    """
    graph = Graph().parse(rdf_filepath)
    return graph


def get_store(filename: str = getenv('LOCAL_RDF_STORE_FILENAME')) -> rdflib.Graph:
    """Retrieve the existing metadata store if it exists. Otherwise create a new one.

    :param filename: Optional filename for the local metadata store (defaults to env)

    :return: The graph metadata store.
    :rtype: rdflib.Graph
    """
    local_file_path: str = join(getenv('LOCAL_DATA_DIR'), filename)
    if os.path.isfile(local_file_path):
        return load_store(local_file_path)
    else:
        print(f'No local metadata store found ({local_file_path}), trying to fetch it from the S3 bucket...')
        try:
            get_object_from_s3(object_key=getenv('LOCAL_RDF_STORE_FILENAME'))
            return load_store(local_file_path)
        except botocore.exceptions.ClientError:
            print('No metadata store found in S3 bucket, creating a new store.')
            return create_new_store()


def save_store(graph: rdflib.Graph, filename: str = getenv('LOCAL_RDF_STORE_FILENAME')):
    """ Save the metadata store to disk and to S3.

    :param graph: The graph to store on disk and in the S3 bucket
    :param filename: Optional filename for the local metadata store (defaults to env)
    """
    local_file_path: str = join(getenv('LOCAL_DATA_DIR'), filename)
    graph.serialize(destination=local_file_path)
    put_object_to_s3(filepath=local_file_path)







