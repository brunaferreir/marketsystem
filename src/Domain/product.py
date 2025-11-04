class ProductDomain:
    def __init__(self, name, price, quantity, status, image_path, user_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.image_path = image_path
        self.user_id = user_id

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "image_path": self.image_path,
            "user_id": self.user_id
        }
