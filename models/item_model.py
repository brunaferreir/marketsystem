from entities.item import item
class ItemModel:
    def __init__(self):
        self.items = []
        self.max_id = 1

    def add(self, nome):
        new_item = item(self.max_id, nome)
        self.items.append(new_item)
        self.max_id +=1
        return new_item
    
    def get_all(self):
        return self.items