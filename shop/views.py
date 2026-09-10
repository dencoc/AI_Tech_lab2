from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from .models import Product, Customer, Purchase


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        return render(request, 'shop/buy.html', {
            'product': product
        })

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        name = request.POST.get('name')
        address = request.POST.get('address')

        customer, created = Customer.objects.get_or_create(
            name=name,
            address=address
        )

        discount = customer.get_discount()

        price = product.price
        final_price = price * (100 - discount) // 100

        Purchase.objects.create(
            product=product,
            customer=customer
        )

        return HttpResponse(
            f'Спасибо за покупку, {customer.name}! '
            f'Скидка: {discount}%. '
            f'К оплате: {final_price} руб.'
        )