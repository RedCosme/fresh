from django.urls import path

from goods.views import index, list, detail


app_name = "goods"
urlpatterns = [
    path("index/", index, name="index"),
    path("list/<int:category_id>/<str:sort>/", list, name="list"),
    # 商品的详情页
    path("detail/<int:goods_id>/", detail, name="detail")
]