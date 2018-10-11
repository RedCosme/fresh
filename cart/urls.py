from django.urls import path

from cart.views import cart, add, delete, update


app_name = "cart"
urlpatterns = [
    path("", cart, name="cart"),
    path("add/<int:goods_id>/<int:count>/", add, name="add"),
    path("delete/<int:cart_id>/", delete, name="delete"),
    path("update/<int:cart_id>/<int:count>/", update, name="update")
]