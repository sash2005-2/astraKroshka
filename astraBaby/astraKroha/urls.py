from django.urls import path, re_path

from django.views.generic import TemplateView

from .views import (
    index,
    product_view,
    category_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    update_qty,
    checkout_view,
    order_create_view,
    make_order_view,
    about_view, contact_view, pay_view, delivery_view)


urlpatterns = [
    re_path(r'category/(?P<category_slug>[-\w]+)/$', category_view, name='category_view_url'),
    re_path(r'product/(?P<product_slug>[-\w]+)/$', product_view, name='product_view_url'),
    path('add_to_cart/$', add_to_cart_view, name='add_to_cart_view_url'),#(?P<product_slug>[-\w]+)/
    path('remove_from_cart_view/$', remove_from_cart_view, name='remove_from_cart_url'),#re_path(r'remove_from_cart_view/(?P<product_slug>[-\w]+)/$', remove_from_cart_view, name='remove_from_cart_url'),
    path('update_qty/', update_qty, name='update_qty_url'),
    path('cart/', cart_view, name='cart_view_url'),
    path('checkout/', checkout_view, name='checkout_view_url'),
    path('order/', order_create_view, name='order_create_view_url'),
	path('make_order/', make_order_view, name='make_order_url'),
    path('thank_you/', TemplateView.as_view(template_name='astraKroha/thank_you.html'), name='thank_you'),
	path('about/', about_view, name='about_url'),
	path('contact/', contact_view, name='contact_url'),
	path('pay/', pay_view, name='pay_url'),
	path('delivery/', delivery_view, name='delivery_url'),
    path('', index, name='index_url'),
]
