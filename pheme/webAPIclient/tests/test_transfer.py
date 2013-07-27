import shutil
import unittest
import tempfile

from pheme.webAPIclient.transfer import Distribute_client, PHINMS_client
from pheme.webAPIclient.archive import document_store

lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing
elit. Aliquam placerat libero velit, non laoreet arcu feugiat
vel. Praesent viverra aliquam dolor, nec commodo mauris fermentum
id. Aliquam semper metus nulla, et venenatis velit tempor quis. Nunc
ornare sed metus tristique auctor. Vivamus varius lacinia est, eget
ultrices nulla. Donec et dui nunc. Praesent elementum massa velit,
eget blandit lorem placerat sed. Mauris accumsan ipsum vitae lorem
luctus pretium. Ut hendrerit nibh ut quam pretium, et ultrices dui
sollicitudin. Vestibulum ante ipsum primis in faucibus orci luctus et
ultrices posuere cubilia Curae; Nam in tincidunt erat. Morbi ut mauris
feugiat, aliquam lacus rhoncus, cursus augue."""


class TestDistribute_client(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testZippedUpload(self):
        "Can we upload a zipped copy"
        tmpfile = tempfile.NamedTemporaryFile('w')
        tmpfile.write(lorem_ipsum)
        tmpfile.seek(0)
        metadata = {'reportable_region': 'test_region', }
        doc_id = document_store(tmpfile.name,
                                document_type='essence',
                                compress_with=Distribute_client.ZIP_PROTOCOL,
                                **metadata)
        self.assertTrue(doc_id)
        agent = Distribute_client(zip_first=True)
        self.assertFalse(agent.transfer_file(doc_id))

    def testUnZippedUpload(self):
        "Can we upload an unzipped copy"
        tmpfile = tempfile.NamedTemporaryFile('w')
        tmpfile.write(lorem_ipsum)
        tmpfile.seek(0)
        metadata = {'reportable_region': 'wasc', }
        doc_id = document_store(tmpfile.name,
                                document_type='essence',
                                **metadata)
        self.assertTrue(doc_id)
        agent = Distribute_client(zip_first=False)
        self.assertFalse(agent.transfer_file(doc_id))


class TestPHINMS_client(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testZippedUpload(self):
        "Can we upload a zipped copy"
        tmpfile = tempfile.NamedTemporaryFile('w')
        tmpfile.write(lorem_ipsum)
        tmpfile.seek(0)
        doc_id = document_store(tmpfile.name,
                                document_type='essence',
                                compress_with=None)  # PHINMS_client.ZIP_PROTOCOL)
        self.assertTrue(doc_id)
        agent = PHINMS_client(zip_first=True)
        self.assertFalse(agent.transfer_file(doc_id))

    def testUnZippedUpload(self):
        "Can we upload an unzipped copy"
        tmpfile = tempfile.NamedTemporaryFile('w')
        tmpfile.write(lorem_ipsum)
        tmpfile.seek(0)
        doc_id = document_store(tmpfile.name,
                                document_type='essence',
                                compress_with=None)
        self.assertTrue(doc_id)
        agent = PHINMS_client(zip_first=False)
        self.assertFalse(agent.transfer_file(doc_id))
