from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_purchase_count(self):
        return self.purchase_set.count()

    def get_discount(self):
        purchase_count = self.get_purchase_count()

        if purchase_count >= 20:
            return 15
        elif purchase_count >= 10:
            return 10
        elif purchase_count >= 5:
            return 5

        return 0


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def get_discount(self):
        return self.customer.get_discount()

    def get_price_with_discount(self):
        discount = self.get_discount()
        return self.product.price * (100 - discount) // 100

    def __str__(self):
        return f'{self.customer} — {self.product}'