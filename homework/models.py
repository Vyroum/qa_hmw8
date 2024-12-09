from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, quantity) -> bool:

        if self.quantity >= quantity:
            return True
        else:
            return False

    def buy(self, quantity):

        if not self.check_quantity(quantity):
            raise ValueError(f"Недостаточно товара '{self.name}' на складе.")
        self.quantity -= quantity

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):

        if buy_count > product.quantity:
            raise ValueError(f"Недостаточно {product.name} для добавления в корзину ")
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        if product in self.products:
            if remove_count is None or remove_count >= self.products[product]:
                del self.products[product]
            else:
                self.products[product] -= remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total_sum = sum(product.price * quantity for product, quantity in self.products.items())
        return total_sum

    def buy(self):

        for product, quantity in self.products.items():
            if quantity > product.quantity:
                raise ValueError(f"Недостаточно {product.name} для покупки")
        for product, quantity in self.products.items():
            product.quantity -= quantity
        self.clear()
