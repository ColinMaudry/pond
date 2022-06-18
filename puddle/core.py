from .utils import *
from metadata_store import PREFIXES
from datetime import datetime


def create_dataset(urls: [str] or str, dataset_series_id: str, fileexts: [str] or str):
    """Create a dataset from data URLS, link it to a dataset series, and push the files to S3.

    :param urls: The URLs to download the data (or single URL)
    :param dataset_series_id: The dataset will belong to this dataset series.
    :param fileexts: For each URL, the file extension that will be given to the final file.
    :return: Metadata about the file
    """

    dataset_date: str = datetime.now().isoformat()
    dataset_id: str = f"{dataset_series_id}_{dataset_date}"

    # download the files
    if isinstance(urls, str) and isinstance(fileexts, str):
        urls = [urls]
        fileexts = [fileexts]
        
    if len(urls) != len(fileexts):
        print('You must provide the same number of URLs and file extensions.')
        raise ValueError

    files = []
    for i, url in enumerate(urls):
        files.append(download_file(url=url, fileext=fileexts[i], dataset_series_id=dataset_series_id))

    # TODO analyze the files: number of lines, columns, profiling


    # create a new dataset with the provided info
    turtle = PREFIXES + f"""
    :{dataset_series_id}_{dataset_date} a dcat:Dataset;
    dcterms:identifier "{dataset_id}";
    dcterms:created "{dataset_date}";
    dcat:inSeries :{dataset_series_id} .  
    """





    # create the distributions and link the dataset

    # create a new data series if needed and link the dataset

    # push the files to S3

    # add the dataset graph to the main graph store

    # save the graph store
    pass

