import grpc, sys, os
sys.path.append(os.path.dirname(__file__) + '/..')
sys.path.append(os.path.dirname(__file__) + '/../service')
from service import inventory_service_pb2, inventory_service_pb2_grpc

class InventoryClient():
    def __init__(self, address='localhost:17624'):
        self.address = address

    def create_book(self, isbn: str, title: str, author: str, genre: str, publishing_year: int) -> bool:
        book = inventory_service_pb2.Book(isbn=isbn,
                                          title=title,
                                          author=author,
                                          genre=genre,
                                          publishing_year=publishing_year)
        with grpc.insecure_channel(self.address) as channel:
            stub = inventory_service_pb2_grpc.InventoryServiceStub(channel)
            response = stub.CreateBook(inventory_service_pb2.CreateBookRequest(book=book))
        if response.status == inventory_service_pb2.STATUS_SUCCESS:
            return True
        return False

    def get_book(self, isbn: str) -> None:
        with grpc.insecure_channel(self.address) as channel:
            stub = inventory_service_pb2_grpc.InventoryServiceStub(channel)
            response = stub.GetBook(inventory_service_pb2.GetBookRequest(isbn=isbn))
        if response.status != inventory_service_pb2.STATUS_SUCCESS:
            return None
        return response.item
