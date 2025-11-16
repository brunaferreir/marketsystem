class ProductDomain:
  def __init__(self, name, price, quantity, status, image_url, seller_id):
    self.name = name
    self.price = price
    self.quantity = quantity
    self.status = status
    self.image_url = image_url
    self.seller_id = seller_id
    
  def to_dict(self):
    return {
      "name": self.name,
      "price": self.price,
      "quantity": self.quantity,
      "status": self.status,
      "image_url": self.image_url,
      "seller_id": self.seller_id
    }