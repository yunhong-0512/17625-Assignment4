from inventory_client import InventoryClient

def batch_query_book(client: InventoryClient, isbns: list[str]):
    res = []
    for isbn in isbns:
        tmp = client.get_book(isbn)
        if tmp is None:
            continue
        res.append(tmp)
    return res

if __name__ == '__main__':
    client = InventoryClient()
    isbns = ['keaippb', 'keaicmp']
    res = batch_query_book(client, isbns)
    for item in res:
        print(item)