from datetime import datetime
from tempfile import NamedTemporaryFile
import os
import unittest

from pheme.webAPIclient.archive import document_store
from pheme.webAPIclient.archive import document_fetch_metadata
from pheme.webAPIclient.archive import document_delete
from pheme.webAPIclient.archive import document_find


class TestArchiveAPI(unittest.TestCase):
    """These hit the configured PHEME archive - must be up to run"""

    def setUp(self):
        self.doc_list = []  # clean up any docs in list on teardown
        self.test_text = "A day in the life..."
        with NamedTemporaryFile('w', delete=False) as self.tempfile:
            self.tempfile.write(self.test_text)

    def tearDown(self):
        os.remove(self.tempfile.name)
        for doc in self.doc_list:
            document_delete(doc)

    def testDocumentArchiveAPI(self):
        "Use client API to store, fetch and delete a document"
        doc_id = document_store(self.tempfile.name, 'longitudinal')
        self.doc_list.append(doc_id)
        self.assertTrue(doc_id)

        # Pull from the store and see if metadata stuck
        metadata = document_fetch_metadata(doc_id)
        self.assertEqual(metadata.get('report_type', None),
                         'longitudinal')

    def testGzipCompression(self):
        "Use client API to compress and store a doc"
        doc_id = document_store(document=self.tempfile.name,
                                document_type='longitudinal',
                                compress_with='gzip')
        self.doc_list.append(doc_id)

        # Pull from the store and see if compressed
        metadata = document_fetch_metadata(doc_id)
        self.assertEqual(metadata.get('compression', None),
                         'gzip')
        filename = os.path.basename(self.tempfile.name) + '.gz'
        self.assertEqual(self.test_text,
                         document_find({'filename': filename}))

    def testZipCompression(self):
        "Use client API to compress and store a doc"
        doc_id = document_store(document=self.tempfile.name,
                                document_type='longitudinal',
                                compress_with='zip')
        self.doc_list.append(doc_id)

        # Pull from the store and see if compressed
        metadata = document_fetch_metadata(doc_id)
        self.assertEqual(metadata.get('compression', None),
                         'zip')
        filename = os.path.basename(self.tempfile.name) + '.zip'
        self.assertEqual(self.test_text,
                         document_find({'filename': filename}))

    def testDocumentArchiveMetaData(self):
        "Persist and test additional metadata with a document"
        now = datetime.now()
        metadata = {'include_updates': True, 'jon': 'bon',
                    'report_type': 'foo', 'time_of_day': now}
        doc_id = document_store(self.tempfile.name, 'longitudinal',
                                **metadata)
        self.doc_list.append(doc_id)
        self.assertTrue(doc_id)

        # Pull from the store and see if metadata stuck
        metadata = document_fetch_metadata(doc_id)
        self.assertEqual(metadata['include_updates'], True)
        self.assertEqual(metadata['jon'], 'bon')
        self.assertEqual(metadata['time_of_day'], now.isoformat())

    def testFindOne(self):
        "Use client API to find a single doc after storing"
        doc_id = document_store(document=self.tempfile.name,
                                document_type='longitudinal')
        self.doc_list.append(doc_id)

        # Pull from the store and see if compressed
        filename = os.path.basename(self.tempfile.name)
        criteria = {'filename': filename}
        document = document_find(criteria)
        self.assertEquals(document, self.test_text)

    def testDuplicate(self):
        "Use client API to store near duplicates and find"
        doc_id = document_store(document=self.tempfile.name,
                                document_type='longitudinal')
        duplicate_id = document_store(document=self.tempfile.name,
                                      document_type='longitudinal',
                                      allow_duplicate_filename=True)
        self.doc_list.append(doc_id)
        self.doc_list.append(duplicate_id)

        criteria = {'filename': os.path.basename(self.tempfile.name)}
        results = document_find(criteria)
        self.assertEquals(len(results), 2)
        self.assertNotEquals(results[0]['_id'], results[1]['_id'])

    def testLimit(self):
        "Use client API to store and limit search results"
        doc_id = document_store(document=self.tempfile.name,
                                document_type='longitudinal')
        duplicate_id = document_store(document=self.tempfile.name,
                                      document_type='longitudinal',
                                      allow_duplicate_filename=True)
        self.doc_list.append(doc_id)
        self.doc_list.append(duplicate_id)

        criteria = {'filename': os.path.basename(self.tempfile.name)}
        results = document_find(criteria)
        self.assertEquals(len(results), 2)
        result = document_find(criteria, limit=1)
        # single result returns doc contents
        self.assertEquals(result, self.test_text)


if '__main__' == __name__:
    unittest.main()
