
import json
from .models import Product, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import datetime
from .utils import cartData, guestOrder
from django.shortcuts import render, get_object_or_404
from blog.models import BlogPost
from .models import Brand
from django.contrib import messages


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        customer, order = guestOrder(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.paid = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    messages.success(request, ("We've received your payment!"))
    return JsonResponse('Payment Complete!', safe=False)

# Trial cart update item view


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(product_code=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
# end of cart update item view

# customer


def confirmed(request):
    title_tag = "Confirmed!"
    data = cartData(request)
    cartItems = data['cartItems']
    blogs = BlogPost.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    transactin_id = str(data['order'].transaction_id[0:3])

    orderItem = data['order']
    pk = orderItem.pk

    orderObject = get_object_or_404(Order, pk=pk)
    paid_status = data['order'].paid

    if paid_status:
        print(f"Order #{orderObject.pk} Paid.")
    else:
        print(f"Order #{orderObject.pk} Not paid.")

    context = {
        'title_tag': title_tag,
        'cartItems': cartItems,
        'blogs': blogs,
        'transactin_id': transactin_id,
        'brands': brands,
    }

    return render(request, 'checkout/confirmed.html', context)
