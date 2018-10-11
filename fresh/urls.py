"""fresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 加入user的路由
    path('account/', include("user.urls", namespace="user")),
    # 加入商品的路由
    path('goods/', include("goods.urls", namespace="goods")),
    # 加入购物车的路由
    path('cart/', include("cart.urls", namespace="cart")),
    # 加入订单的路由
    path('order/', include("order.urls", namespace="order"))
]
