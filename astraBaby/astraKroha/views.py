from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal

from astraBaby.settings import EMAIL_HOST_USER
from .forms import OrderForm
from .models import Category, Product, CartItem, Cart, Order


def index(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    #cart = Cart.objects.first()
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
    }
    return render(request, "astraKroha/index.html", context)


def product_view(request, product_slug):
    #cart = Cart.objects.first()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    try:
        product = Product.objects.get(slug=product_slug)
    except:
        product = None
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'astraKroha/product.html', context)


def category_view(request, category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    #cart = Cart.objects.first()
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products_of_category': products_of_category,
        'cart': cart,
    }
    return render(request, 'astraKroha/category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    #cart = Cart.objects.first()
    context = {
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'astraKroha/cart.html', context)


def add_to_cart_view(request):#, product_slug
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    #new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    #if new_item not in cart.item.all():
    #    cart.item.add(new_item)
    #    cart.save()
    #    return redirect('/cart/')
    cart.add_to_cart(product_slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.item.count(), 'cart_total_price': cart.cart_total,})#redirect('/cart/')


def remove_from_cart_view(request):#, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    #for cart_item in cart.item.all():
    #    if cart_item.product == product:
    #        cart.item.remove(cart_item)
    #        cart.save()
    #        return redirect('/cart/')
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.item.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.item.count(), 'cart_total_price': cart.cart_total})#return redirect('/cart/')


def update_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({
        'cart_total': cart.item.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total
    })


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
    }
    temp = "позиции и количество: "
    for item in cart.item.all():
        temp += item.product.title + " - " + str(item.qty) + "шт. "
    email_body = "заказ№" + str(cart.id) + " на сумму: " + str(cart.cart_total) + "руб. Детали: " + temp
    email = EmailMessage('Subject', email_body, EMAIL_HOST_USER, to=['sash2005-2@yandex.ru'])
   # email.send()
    return render(request, 'astraKroha/checkout.html', context)


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()
    context = {
        'form': form,
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'astraKroha/order.html', context)



def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.item.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order()
        new_order.user=request.user
        new_order.save()
        new_order.items.add(cart)
        new_order.first_name=name
        new_order.last_name=last_name
        new_order.phone=phone
        new_order.address=address
        new_order.buying_type=buying_type
        new_order.comments=comments
        new_order.total = cart.cart_total
        new_order.save()
        del request.session['cart_id']
        del request.session['total']
        return redirect(reverse('thank_you'))


def about_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'astraKroha/about.html', context)


def contact_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'astraKroha/contact.html', context)


def pay_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'astraKroha/pay.html', context)


def delivery_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'astraKroha/delivery.html', context)