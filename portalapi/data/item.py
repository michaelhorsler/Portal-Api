class Item:
    def __init__(self, id, customer, salesorder):
        self.id = id
        self.customer = customer
        self.salesorder = salesorder

    @classmethod
    def from_mongodb(cls, list):
        return cls(list['_id'], list['Customer'], list['salesorder'])
