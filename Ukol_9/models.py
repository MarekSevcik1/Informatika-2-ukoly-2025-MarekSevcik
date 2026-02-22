class Product:
    """
    Reprezentuje produkt ve skladu.
    """
    def __init__(self, name: str, price: float, quantity: int):
        # TODO: Inicializace, využití properties pro validaci
        self._name = name
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        # TODO: Validace, raise ValueError pokud < 0
        if value < 0:
            raise ValueError
        else:
            self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        # TODO: Validace
        if value < 0:
            raise ValueError
        else:
            self._quantity = value

    def to_dict(self) -> dict:
        """Vrátí slovníkovou reprezentaci pro JSON."""
        return {
            "name": self._name,
            "price": self._price,
            "quantity": self._quantity
        }

    @staticmethod
    def from_dict(data: dict) -> 'Product':
        """Vytvoří instanci Product ze slovníku."""
        return Product(data['name'], data['price'], data['quantity'])

    def __str__(self) -> str:
        # TODO: Hezký výpis
        return f"Produkt: {self._name}, stoji {self._price} v poctu: {self._quantity} kusu."
    

class Electronics(Product):
    def __init__(self, name, price, quantity, brand):
        super().__init__(name, price, quantity)
        self.brand = brand

    @property
    def brand(self):
        return self._brand
    
    @brand.setter
    def brand(self, jmeno):
        if len(jmeno) <= 0:
            print("Elektronika musi mit znacku")
        else:
            self._brand= jmeno


    def to_dict(self):
        return super().to_dict() + {"brand": self._brand}
    
    def __str__(self):
        return super().__str__() + f"od znacky: {self._brand}"
    

class PerishableProduct(Product):
    def __init__(self, name, price, quantity, expirationDate):
        super().__init__(name, price, quantity)
        self.expirationDate = expirationDate

    @property
    def expirationDate(self):
        return self._expirationDate
    
    @expirationDate.setter
    def expirationDate(self, datum):
        if datum <= 0:
            print("Produkt musi vydrzet alespon jeden den")
        else:
            self._expirationDate= datum

    def to_dict(self):
        return super().to_dict() + {"expiration date": self._expirationDate}
    
    def __str__(self):
        return super().__str__() + f", datum spotreby: {self._expirationDate}"