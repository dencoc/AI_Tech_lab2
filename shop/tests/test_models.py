from django.test import TestCase
from shop.models import Product, Customer, Purchase
from datetime import datetime


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Чайник", price=2500)
        Product.objects.create(name="Сковорода", price=1800)

    def test_correctness_types(self):
        self.assertIsInstance(
            Product.objects.get(name="Чайник").name,
            str
        )
        self.assertIsInstance(
            Product.objects.get(name="Чайник").price,
            int
        )

        self.assertIsInstance(
            Product.objects.get(name="Сковорода").name,
            str
        )
        self.assertIsInstance(
            Product.objects.get(name="Сковорода").price,
            int
        )

    def test_correctness_data(self):
        self.assertEqual(
            Product.objects.get(name="Чайник").price,
            2500
        )
        self.assertEqual(
            Product.objects.get(name="Сковорода").price,
            1800
        )


class CustomerTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Чайник",
            price=2500
        )

        self.customer = Customer.objects.create(
            name="Иванов",
            address="Светлая ул."
        )

    def create_purchases(self, count):
        for _ in range(count):
            Purchase.objects.create(
                product=self.product,
                customer=self.customer
            )

    def test_correctness_types(self):
        self.assertIsInstance(self.customer.name, str)
        self.assertIsInstance(self.customer.address, str)
        self.assertIsInstance(self.customer.get_purchase_count(), int)
        self.assertIsInstance(self.customer.get_discount(), int)

    def test_new_customer_has_no_discount(self):
        self.assertEqual(
            self.customer.get_purchase_count(),
            0
        )
        self.assertEqual(
            self.customer.get_discount(),
            0
        )

    def test_five_purchases_give_five_percent_discount(self):
        self.create_purchases(5)

        self.assertEqual(
            self.customer.get_purchase_count(),
            5
        )
        self.assertEqual(
            self.customer.get_discount(),
            5
        )

    def test_ten_purchases_give_ten_percent_discount(self):
        self.create_purchases(10)

        self.assertEqual(
            self.customer.get_purchase_count(),
            10
        )
        self.assertEqual(
            self.customer.get_discount(),
            10
        )

    def test_twenty_purchases_give_fifteen_percent_discount(self):
        self.create_purchases(20)

        self.assertEqual(
            self.customer.get_purchase_count(),
            20
        )
        self.assertEqual(
            self.customer.get_discount(),
            15
        )


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Чайник",
            price=2500
        )

        self.customer = Customer.objects.create(
            name="Иванов",
            address="Светлая ул."
        )

        self.datetime = datetime.now()

        Purchase.objects.create(
            product=self.product,
            customer=self.customer
        )

    def test_correctness_types(self):
        purchase = Purchase.objects.get(
            product=self.product
        )

        self.assertIsInstance(purchase.product, Product)
        self.assertIsInstance(purchase.customer, Customer)
        self.assertIsInstance(purchase.date, datetime)

    def test_correctness_data(self):
        purchase = Purchase.objects.get(
            product=self.product
        )

        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.customer, self.customer)

    def test_purchase_count(self):
        self.assertEqual(
            self.customer.get_purchase_count(),
            1
        )

    def test_price_with_discount(self):
        for _ in range(4):
            Purchase.objects.create(
                product=self.product,
                customer=self.customer
            )

        discount = self.customer.get_discount()
        final_price = (
            self.product.price * (100 - discount) // 100
        )

        self.assertEqual(discount, 5)
        self.assertEqual(final_price, 2375)