from django.shortcuts import render

from user.utils import login_required
from user.models import UserModel
from cart.models import CartModel
# Create your views here.


@login_required
def order(request):
    """订单页面"""
    user_id = request.session.get("user_id")
    user = UserModel.objects.get(id=user_id)

    cart_id_list = request.GET.getlist("cart_id_list")

    #根据购物车的id，查询出对应的商品
    cart_info_list = []
    for cart_id in cart_id_list:
        cart = CartModel.objects.get(id=cart_id)
        cart_info_list.append(cart)

    context = {
        "title": "订单页面",
        "user": user,
        "cart_info_list": cart_info_list
    }
    return render(request, "order/order.html", context)
