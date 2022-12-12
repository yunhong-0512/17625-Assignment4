from inventory_service_pb2 import *
from concurrent import futures
import inventory_service_pb2_grpc
import itertools
import logging
import grpc

class BookDB:
    def __init__(self, hardcode=True):
        self.db = {}
        self.cnt = itertools.count(1)
        if hardcode:
            book1 = Book(isbn='keaippb', title='wonderful ppb', author='ppb', genre='poetry', publishing_year=1998)
            self.put(book1)
            book2 = Book(isbn='keaicmp', title='wonderful cmp', author='cmp', genre='poetry', publishing_year=1998)
            self.put(book2)

    def put(self, book: Book) -> bool:
        if book.isbn in self.db:
            return False
        pkey = next(self.cnt)
        self.db[book.isbn] = InventoryItem(inventory_number=pkey, book=book, status=STATUS_SUCCESS)
        return True

    def get(self, isbn: str) -> None:
        if isbn not in self.db:
            return
        return self.db[isbn]


class InventoryServer(inventory_service_pb2_grpc.InventoryServiceServicer):
    def __init__(self):
        self.book_db = BookDB()

    def CreateBook(self, request, context):
        book = request.book
        if self.book_db.put(book):
            return CreateBookResponse(status=STATUS_SUCCESS)
        return CreateBookResponse(status=STATUS_FAILED)

    def GetBook(self, request, context):
        isbn = request.isbn
        content = self.book_db.get(isbn)
        if content is None:
            return GetBookResponse(status=STATUS_FAILED)
        return GetBookResponse(status=STATUS_SUCCESS, item=content)

    @staticmethod
    def serve():
        logging.basicConfig()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        inventory_service_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServer(), server)
        server.add_insecure_port('[::]:17624')
        server.start()
        server.wait_for_termination()

if __name__ == '__main__':
    InventoryServer.serve()