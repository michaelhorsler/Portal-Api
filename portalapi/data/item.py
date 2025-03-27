class Item:
    def __init__(self, id, customer, sales_order, engineer):
        self.id = id
        self.customer = customer
        self.sales_order = sales_order
        self.engineer = engineer

    @classmethod
    def from_mongodb(cls, list):
        return cls(list['_id'], list['Customer'], list['Sales_Order'], list['Engineer'])
