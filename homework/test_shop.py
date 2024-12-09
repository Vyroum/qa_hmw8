import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_2():
    return Product("paperclip", 0.5, "This is a paperclip", 20)


@pytest.fixture
def cart(product):
    return Cart()


buy_count_product_1 = 10
buy_count_product_2 = 5


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(200)
        assert product.quantity == 800

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:

    def test_add_product_to_cart(self, cart, product):
        cart.add_product(product, buy_count_product_1)
        assert cart.products[product] == buy_count_product_1

    def test_add_existing_product_to_cart(self, cart, product):
        cart.add_product(product, buy_count_product_1)
        cart.add_product(product, buy_count_product_1)
        assert cart.products[product] == buy_count_product_1 * 2

    def test_not_enough_product_to_add(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)

    def test_delete_one_product_from_cart(self, cart, product):
        cart.add_product(product, buy_count_product_1)
        cart.remove_product(product, 1)
        assert cart.products[product] == buy_count_product_1 - 1

    def test_delete_whole_quantity_product_from_cart(self, cart, product):
        cart.add_product(product, buy_count_product_1)
        cart.remove_product(product, remove_count=buy_count_product_1)
        assert len(cart.products) == 0

    def test_delete_all_product_from_cart(self, cart, product, product_2):
        cart.add_product(product, buy_count_product_1)
        cart.add_product(product_2, buy_count_product_2)
        cart.remove_product(product)
        cart.remove_product(product_2)
        assert product and product_2 not in cart.products

    def test_delete_one_product_whole_quantity(self, cart, product, product_2):
        cart.add_product(product, buy_count_product_1)
        cart.add_product(product_2, buy_count_product_2)
        cart.remove_product(product, remove_count=buy_count_product_1)
        assert product not in cart.products and cart.products[product_2] == buy_count_product_2

    def test_clear_cart(self, cart, product):
        cart.add_product(product, buy_count_product_1)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product, product_2):
        cart.add_product(product, buy_count_product_1)
        cart.add_product(product_2, buy_count_product_2)
        total_price = cart.get_total_price()
        assert total_price == (buy_count_product_1 * product.price) + (buy_count_product_2 * product_2.price)

    def test_buy_cart_success(self, cart, product, product_2):
        product_storage_quantity = product.quantity
        product_2_storage_quantity = product_2.quantity
        cart.add_product(product, buy_count_product_1)
        cart.add_product(product_2, buy_count_product_2)
        cart.buy()
        assert product.quantity == product_storage_quantity - buy_count_product_1
        assert product_2.quantity == product_2_storage_quantity - buy_count_product_2

    def test_buy_cart_error_with_not_enough_quantity(self, cart, product, product_2):
        cart.add_product(product_2, buy_count_product_2)
        with pytest.raises(ValueError):
            cart.add_product(product, product.quantity + 1)
            cart.buy()
