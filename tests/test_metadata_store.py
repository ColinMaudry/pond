from pond import *
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, DCAT

test_filename = 'test_metadata_store.ttl'


def get_rdf_format_file_extension(file_format: str) -> str:
    mapping = {
        'turtle': 'ttl',
        'n3': 'n3',
        'rdf': 'rdf'
    }
    return mapping[file_format]


def test_create_store():
    graph = create_new_store()
    graph.add(
        (URIRef('uri:subject'),
         RDF.type,
         DCAT.Dataset)
    )
    graph.add(
        (
            URIRef('uri:subject'),
            DCAT.byteSize,
            Literal(1000)
        )
    )

    # Save to store with filename as filename + file extension based on serialization
    save_store(graph, test_filename)

    assert True


def test_retrieve_store_on_disk():
    graph = get_store(test_filename)
    print(graph.serialize())

    assert (URIRef('uri:subject'), DCAT.byteSize, Literal(1000)) in graph
