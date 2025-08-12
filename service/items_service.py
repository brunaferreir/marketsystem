from models.item_model import ItemModel
class ItemService:
    def __init__(self):
        self.model = ItemModel()

    # def add (self, nome):
    #     return self.model.add(nome).to_dict()

    def add(self, name):
        new_item = self.model.add(name)
        return new_item.to_dict()

    def get_all(self):
        items = self.model.get_all()
        return [item.to_dict() for item in items]









































