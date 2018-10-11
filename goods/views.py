from django.shortcuts import render
from django.core.paginator import Paginator

from goods.models import CategoryModel, CategoryGoodsModel, GoodsModel
from cart.models import CartModel
from common.common import cart_count_goods
# Create your views here.


def index(request):
    """主页"""
    # 拿出所有的分类
    category_list = CategoryModel.objects.all()
    # 分别取出分类下的最新的商品
    new_goods_dict = {} # 存储每个分类下的最新的商品
    for category in category_list:
        # goods_list = CategoryGoodsModel.objects.filter(category_id=category.id).order_by("-goods_id")[:4]
        # 拿到查询出的所有的goods的id
        # goods_ids = [goods.goods_id for goods in goods_list]
        # print(goods_ids)
        # 修改了商品model之后的逻辑
        # 直接通过商品分类id从goods中获取当前分类的商品
        goods_info_list = GoodsModel.objects.filter(category_id=category.id).order_by("-id")[:4]
        print(goods_info_list)
        new_goods_dict[category] = goods_info_list

    # 从session中拿到user的id
    cart_count = cart_count_goods(request, CartModel)

    context = {
        "new_goods_dict": new_goods_dict,
        "cart_count": cart_count
    }
    print(context)
    return render(request, "goods/index.html", context)


def list(request, category_id, sort, page_num):
    """商品列表视图"""
    """category_id: 分类的id
       page_num: 获取当前页的页码
       sort: 排序字段（默认：default, 价格：price, 人气: popular）"""
    category = CategoryModel.objects.get(id=category_id)
    # 取该类型最新的两个商品
    news = GoodsModel.objects.filter(category_id=category_id).order_by("-id")[:2]
    # 外键的用法
    # news = category.goodsmodel_set.order_by("-id")[:2]\
    goods_list = []
    if sort == "default": # 默认排序，最新在上面
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by("-id")
    elif sort == "price": # 按价格排序
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by("-price")
    elif sort == "popular":  # 按人气排序
        goods_list = GoodsModel.objects.filter(category_id=category_id).order_by("-popular")

    # 根据商品的列表goods_list 进行分页
    paginator = Paginator(goods_list, 2)
    page = paginator.page(page_num)

    cart_count = cart_count_goods(request, CartModel)
    context = {
        "category": category, # 商品的分类对象
        "news": news, # 新品推荐
        "goods_list": goods_list, # 排序后的商品列表
        "sort": sort, # 排序的条件
        "cart_count": cart_count, # 购物车中的商品数量
        "page": page,
        "page_num": page_num, # 当前的页数
    }

    return render(request, "goods/list.html", context)


def detail(request, goods_id):
    """某个商品的详细信息 goods_id是具体的某个商品"""
    goods = GoodsModel.objects.get(id=goods_id)
    goods.popular = goods.popular + 1 # 增加商品的人气值
    goods.save()
    # news = GoodsModel.objects.filter(category_id=goods.category_id).order_by("-id")[:2]
    # 利用orm外键的特性
    news = goods.category.goodsmodel_set.order_by("-id")[:2]

    # 购物车内商品的数量
    cart_count = cart_count_goods(request, CartModel)

    # 记录最近的浏览记录，在用户中心使用
    # 判断是否已经登陆
    if request.session.has_key("user_id"):
        user_id = str(request.session.get("user_id"))
        goods_id_list = request.session.get(user_id, [])
        if not goods_id_list:  # 判断是否有浏览记录
            goods_id_list.append(goods.id)
        else:
            # 如果已经存在过浏览的商品，删除掉这一个
            if goods_id in goods_id_list:
                goods_id_list.remove(goods_id)
            goods_id_list.insert(0, goods_id) # 添加元素到列表的第一个
            if len(goods_id_list) > 5:  # 如果超过5个浏览记录删除最后一个
                del goods_id_list[-1]
        # 把最近浏览的商品存储在session中 以user_id的值为key
        request.session[user_id] = goods_id_list
    return render(request, "goods/detail.html", {"goods": goods, "news": news, "cart_count": cart_count})
