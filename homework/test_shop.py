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


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False
        pass

    def test_product_buy(self, product):
        product.buy(200)
        assert product.quantity == 800

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:

    def test_add_product_to_cart(self, cart, product):
        cart.add_product(product, 10)
        assert cart.products[product] == 10

    def test_not_enough_product_to_add(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, 1001)

    def test_delete_one_product_from_cart(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 1)
        assert cart.products[product] == 9

    def test_delete_all_product_from_cart(self, cart, product, product_2):
        cart.add_product(product, 10)
        cart.add_product(product_2, buy_count=5)
        cart.remove_product(product)
        cart.remove_product(product_2)
        assert product and product_2 not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 10)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product, product_2):
        cart.add_product(product, 20)
        cart.add_product(product_2, 10)
        total_price = cart.get_total_price()
        assert total_price == (20 * 100) + (10 * 0.5)

    def test_buy_cart_success(self, cart, product, product_2):
        cart.add_product(product, 10)
        cart.add_product(product_2, buy_count=20)
        cart.buy()
        assert product.quantity == 990 and product_2.quantity == 0

    def test_buy_cart_error_with_not_enough_quantity(self, cart, product):
        with pytest.raises(ValueError):
            cart.add_product(product, 1001)
            cart.buy()
