from portalapi.data.item import Item

class viewmodel:
    def __init__(self, items: list[Item]):
        self._items = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def engineer_items(self):
        engineer_items = list(filter(lambda item: item.engineer != "", self._items))
        return engineer_items
    
    @property
    def salesorder_items(self):
        salesorder_items = list(filter(lambda item: item.sales_order != "", self._items))
        return salesorder_items
    
    @property
    def customer_items(self):
        customer_items = list(filter(lambda item: item.customer != "", self._items))
        return customer_items