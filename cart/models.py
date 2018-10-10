from django.db import models
from django.contrib import admin
# Create your models here.
from user.models import UserModel
from goods.models import GoodsModel


class CartModel(models.Model):
    """购物车"""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="用户")
    goods = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, verbose_name="商品")
    count = models.IntegerField(default=1, verbose_name="商品数量")

    class Meta:
        db_table = "cart"
        verbose_name = "购物车"
        verbose_name_plural = verbose_name


@admin.register(CartModel)
class CartAdminModel(admin.ModelAdmin):
    list_display = ("user", "goods", "count")
