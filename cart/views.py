from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from shop.models import Product, Coupon
from .cart import Cart
from .forms import CartAddProductForm, CouponApplyForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@require_POST
def cart_apply_coupon(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session[settings.COUPON_SESSION_ID] = coupon.id
        except Coupon.DoesNotExist:
            request.session[settings.COUPON_SESSION_ID] = None
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    coupon_apply_form = CouponApplyForm()  # 新增折扣碼表單
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    })