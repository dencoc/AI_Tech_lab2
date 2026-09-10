from django.test import TestCase, Client
from shop.models import Product, Customer, Purchase


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.product = Product.objects.create(
            name="Чайник",
            price=2500
        )

    def test_webpage_accessibility(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_purchase_page_accessibility(self):
        response = self.client.get(
            f'/buy/{self.product.id}/'
        )

        self.assertEqual(response.status_code, 200)

    def test_purchase_creation(self):
        response = self.client.post(
            f'/buy/{self.product.id}/',
            {
                'name': 'Иванов',
                'address': 'Светлая ул.'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 1)

        purchase = Purchase.objects.first()

        self.assertEqual(
            purchase.product,
            self.product
        )
        self.assertEqual(
            purchase.customer.name,
            'Иванов'
        )
        self.assertEqual(
            purchase.customer.address,
            'Светлая ул.'
        )

    def test_customer_purchase_count(self):
        self.client.post(
            f'/buy/{self.product.id}/',
            {
                'name': 'Иванов',
                'address': 'Светлая ул.'
            }
        )

        self.client.post(
            f'/buy/{self.product.id}/',
            {
                'name': 'Иванов',
                'address': 'Светлая ул.'
            }
        )

        customer = Customer.objects.get(
            name='Иванов',
            address='Светлая ул.'
        )

        self.assertEqual(
            customer.get_purchase_count(),
            2
        )