import requests
import logging

from pheme.util.config import Config


def transfer_document(document_id, transfer_agent,
                      compress_with=None):
    """Web API client call to request transfer of given document ID

    :param document_id: the document ID to transfer, likely returned
      from a document_store() call on the same Web API

    :param transfer_agent: such as 'phin-ms' or 'distribute'.

    :param compress_with: if additional compression is desired, this
      may be set to 'zip' or 'gzip', to be performed before sending.

    """
    query_params = dict()
    if compress_with is not None:
        query_params['compress_with'] = compress_with

    config = Config()
    parts = dict()
    parts['doc'] = document_id
    parts['host'] = config.get("WebAPI", "host")
    parts['port'] = config.get("WebAPI", "port")
    parts['agent'] = transfer_agent

    url = 'http://%(host)s:%(port)s/%(agent)s/%(doc)s' % parts
    if query_params:
        url = url + '?' +\
            '&'.join([k+'='+v for k, v in query_params.items()])

    # Initiate request, wait on response
    r = requests.post(url)
    if r.status_code != 200:  # pragma no cover
        failure = "Failed POST (%d) for transfer request: %s" %\
            (r.status_code, url)
        logging.error(failure)
        logging.error(r.text)
        raise RuntimeError(failure)


class Transfer_client(object):
    """Base class for transfer clients"""

    def __init__(self, zip_first=False):
        """Initialize state

        :param zip_first: if set, instruct the transfer agent to
          first compress before sending, using self.ZIP_PROTOCOL.

        """
        self.compress_with = self.ZIP_PROTOCOL if zip_first else None

    def transfer_file(self, file):
        """Trigger webAPIclient to transfer

        :param file: PHEME webAPI archive document id to send.

        """
        logging.info("initiate transfer request for %s using %s",
                     file, self.TRANSFER_AGENT)
        transfer_document(file,
                          transfer_agent=self.TRANSFER_AGENT,
                          compress_with=self.compress_with)
        logging.info("completed transfer request for %s using %s",
                     file, self.TRANSFER_AGENT)


class Distribute_client(Transfer_client):
    """Initiate request for transfer of report to distribute.

    Maintains details for transfering reports to distribute.
    transfer_file() calls the webAPIclient library to send the
    persisted document, which uploads files to Distribute's https
    server.

    """
    ZIP_PROTOCOL = 'gzip'
    TRANSFER_AGENT = 'distribute'


class PHINMS_client(Transfer_client):
    """Initiate request for transfer of report via PHINMS.

    Maintains details for transfering reports to a configured PHINMS
    server.  transfer_file() calls the webAPIclient library to send
    the persisted document, by dropping a copy of the file in the
    appropriate directory PHINMS is set to poll.

    """
    ZIP_PROTOCOL = 'zip'
    TRANSFER_AGENT = 'phin-ms'
