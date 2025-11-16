class SaleDomain:
  def __init__(self, product_id, seller_id, quantity, price_at_sale):
    self.product_id = product_id
    self.seller_id = seller_id
    self.quantity = quantity
    self.price_at_sale = price_at_sale
    
  def to_dict(self):
    return {
      "product_id": self.product_id,
      "seller_id": self.seller_id,
      "quantity": self.quantity,
      "price_at_sale": self.price_at_sale
    }
