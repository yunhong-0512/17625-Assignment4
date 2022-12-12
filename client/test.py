import unittest, subprocess, time
from unittest.mock import Mock
from inventory_client import InventoryClient
from service import inventory_service_pb2
from get_book_titles import batch_query_book

class MockClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = InventoryClient()

    def test_01_mock_without_server(self):
        book1 = inventory_service_pb2.Book(isbn='keaippb', title='wonderful ppb', author='ppb', genre='poetry', publishing_year=1998)
        item1 = inventory_service_pb2.InventoryItem(inventory_number=1, book=book1, status=inventory_service_pb2.STATUS_SUCCESS)
        # mock API client
        self.client.get_book = Mock(side_effect={'keaippb': item1}.get)
        # pass the newly created mock object as a client API accessor
        # without a server running
        res = batch_query_book(self.client, ['keaippb'])
        self.assertEqual(item1.inventory_number, res[0].inventory_number)

    def test_02_mock_without_server(self):
        book1 = inventory_service_pb2.Book(isbn='keaippb', title='wonderful ppb', author='ppb', genre='poetry', publishing_year=1998)
        item1 = inventory_service_pb2.InventoryItem(inventory_number=1, book=book1, status=inventory_service_pb2.STATUS_SUCCESS)
        book2 = inventory_service_pb2.Book(isbn='keaicmp', title='wonderful cmp', author='cmp', genre='poetry', publishing_year=1998)
        item2 = inventory_service_pb2.InventoryItem(inventory_number=2, book=book2, status=inventory_service_pb2.STATUS_SUCCESS)
        # mock API client
        self.client.get_book = Mock(side_effect={'keaippb': item1, 'keaicmp': item2}.get)
        # pass the newly created mock object as a client API accessor
        # without a server running
        res = batch_query_book(self.client, ['keaippb', 'keaicmp'])
        self.assertEqual(item1.inventory_number, res[0].inventory_number)
        self.assertEqual(item2.inventory_number, res[1].inventory_number)

    def test_03_mock_without_server(self):
        # mock API client
        self.client.get_book = Mock(return_value=None)
        # pass the newly created mock object as a client API accessor
        # without a server running
        res = batch_query_book(self.client, ['keaippb'])
        self.assertEqual(0, len(res))

    def test_04_integration_with_server(self):
        cmd = 'exec python3 ../service/InventoryServer.py'
        # using a live server
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
        time.sleep(1)
        res = batch_query_book(self.client, ['keaippb'])
        self.assertEqual(1, res[0].inventory_number)
        proc.kill()

    def test_05_integration_with_server(self):
        cmd = 'exec python3 ../service/InventoryServer.py'
        # using a live server
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
        time.sleep(1)
        res = batch_query_book(self.client, ['keaippb', 'keaicmp'])
        self.assertEqual(1, res[0].inventory_number)
        self.assertEqual(2, res[1].inventory_number)
        proc.kill()

if __name__ == '__main__':
    unittest.main(warnings='ignore', verbosity=2)