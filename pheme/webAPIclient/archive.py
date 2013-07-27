from datetime import datetime
import os
import requests
import json

from pheme.util.config import Config


def url_builder(predicate=None, resource=None, view=None, query_params={}):
    """Build webAPI url from config and passed values

    :param predicate: desired action or type of document
    :param resource: filename or object identifier
    :param view: specilized view, such as metadata
    :param query_params: dictionary of key, values to append

    returns URL ready for request, post, etc.

    """
    config = Config()
    url = 'http://%s:%s' % (config.get("WebAPI", "host"),
                            config.get("WebAPI", "port"))
    if predicate:
        url = '/'.join((url, predicate))
    if resource:
        url = '/'.join((url, resource))
    if view:
        url = '/'.join((url, '@@' + view))
    if query_params:
        url = '?'.join((url,
                        '&'.join([k+'='+v for k, v in query_params.items()])))
    return url


def document_store(document, document_type, compress_with=None,
                   allow_duplicate_filename=False, **metadata):
    """Client call to put document and meta data in PHEME archive

    The PHEME archive exposes a Wep API to PUT documents in the
    document store (database), among other things.  This function
    wraps the HTTP request for easy client code use.

    :param document: the document to persist, a path to the readable
      file on the local filesystem.

    :param document_type: type, such as 'essence', 'gipse', etc.  See
      pheme.webAPI.resources.Root for options.

    :param compress_with: Can be 'gzip' or 'zip' (or None).  Will
      transmit the requested compression of the document prior to store.

    :param allow_duplicate_filename: If set, duplicates will be
      versioned.  By default a duplicate raises an exception.

    :param metadata: Any additional key, value strings to associate
      with the document

    returns the resulting document_id, a key which may be used to
      retrieve the same document.

    """
    url = url_builder(predicate=document_type,
                      resource=os.path.basename(document))

    payload = dict()
    if compress_with:
        payload['compress_with'] = compress_with
    if allow_duplicate_filename:
        payload['allow_duplicate_filename'] = allow_duplicate_filename

    if metadata:
        # special handler for datetime types
        datetime_handler = lambda x: x.isoformat()\
            if isinstance(x, datetime)\
            else None
        payload['metadata'] = json.dumps(metadata, default=datetime_handler)

    with open(document, 'rb') as content:
        files = {os.path.basename(document): content}
        r = requests.put(url, files=files, data=payload)

    if r.status_code != 200:  # pragma no cover
        raise RuntimeError("Failed POST (%d) for store document: "
                           "%s , see PHEME archive log" %
                           (r.status_code, url))

    # Pull the doc id from the json reponse
    response = json.loads("".join([i for i in r.iter_content()]))
    return response['document_id']


def document_delete(document_id):
    """Delete the requested document"""
    r = requests.delete(url_builder(resource=document_id))
    assert(r.status_code == 200)


def document_fetch_metadata(document_id):
    """Returns all metadata from the archived document if found"""
    r = requests.get(url_builder(resource=document_id, view='metadata'))
    return(json.loads(r.text))


def document_find(criteria, limit=0):
    """Search for best matching document(s) in archive

    :param criteria: dictionary of key, values to search for
    :param limit: optional restriction on number or matching docs;
      zero implies no limit

    returns a list of metadata if multiple matches are found.
    returns the document text if only a single match or limit is set to 1.

    """
    query_params = {'query': json.dumps(criteria), 'limit': str(limit)}
    r = requests.get(url_builder(predicate='search',
                                 query_params=query_params))
    return json.loads(r.text)
